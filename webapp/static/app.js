"use strict";
let csrf = "";
const el = id => document.getElementById(id);
function notice(message, error=false) { el("notice").textContent = message; el("notice").classList.toggle("error",error); }
async function call(path, options={}) {
  options.credentials="same-origin";
  if(options.method && options.method!=="GET" && csrf) options.headers={...(options.headers||{}),"X-CSRF-Token":csrf};
  const res=await fetch(path,options);
  const body=await res.json().catch(()=>({detail:"Unexpected response"}));
  if(!res.ok) throw new Error(body.detail||"Request failed");
  return body;
}
function makeItem(title,detail,status) {
  const row=document.createElement("div");row.className="item";
  const col=document.createElement("div");const strong=document.createElement("strong");
  strong.textContent=title;const small=document.createElement("small");small.textContent=detail;
  col.append(strong,small);row.append(col);
  if(status){const badge=document.createElement("span");badge.className="badge";badge.textContent=status;row.append(badge);}
  return row;
}
function populate(id,rows,message,renderer) {
  const root=el(id);root.replaceChildren();
  if(!rows.length){root.textContent=message;return;}
  rows.forEach(row=>root.append(renderer(row)));
}
async function refresh() {
  try {
    const entries=await Promise.all([call("/datasets"),call("/jobs"),call("/models")]);
    const datasets=entries[0],jobs=entries[1],models=entries[2];
    el("dataset-count").textContent=datasets.length;
    el("job-count").textContent=jobs.length;
    el("model-count").textContent=models.length;
    populate("datasets",datasets,"No datasets uploaded.",d=>makeItem(d.name||d.id,"ID: "+d.id,d.status));
    populate("jobs",jobs,"No training jobs yet.",j=>makeItem(j.model_mode||"Job","ID: "+j.id,j.status));
    populate("model-list",models,"No models available.",m=>makeItem(m.mode||"Model","ID: "+m.id,m.published?"Published":"Private"));
    const datasetSel=el("job-dataset");datasetSel.replaceChildren(new Option("Select a dataset",""));
    datasets.filter(d=>d.status==="READY").forEach(d=>datasetSel.add(new Option(d.name||d.id,d.id)));
    const modelSel=el("model-id");modelSel.replaceChildren(new Option("Select a model",""));
    models.filter(m=>m.mode==="radiology").forEach(m=>modelSel.add(new Option(m.id,m.id)));
    el("logout").hidden=false; notice("Workspace synchronized.");
  } catch(e){notice(e.message,true);}
}
function action(fn){Promise.resolve().then(fn).catch(e=>notice(e.message,true));}
el("auth").addEventListener("submit",e=>{
  e.preventDefault();const mode=e.submitter?.dataset.mode||"login";
  action(async()=>{
    const r=await call("/auth/"+mode,{method:"POST",body:new FormData(e.currentTarget)});
    if(mode==="register"){notice("Account created. Sign in to continue.");return;}
    csrf=r.csrf;await refresh();
  });
});
el("logout").addEventListener("click",()=>action(async()=>{await call("/auth/logout",{method:"POST"});location.reload();}));
el("refresh").addEventListener("click",()=>action(refresh));
el("upload-form").addEventListener("submit",e=>{
  e.preventDefault();action(async()=>{
    const f=new FormData();f.append("archive",el("dataset").files[0]);
    const r=await call("/datasets",{method:"POST",body:f});
    notice("Dataset uploaded: "+r.dataset_id);await refresh();
  });
});
el("job-form").addEventListener("submit",e=>{
  e.preventDefault();action(async()=>{
    const f=new FormData();f.append("dataset_id",el("job-dataset").value);f.append("model_mode",el("job-mode").value);
    const r=await call("/jobs",{method:"POST",body:f});
    notice("Queued training job: "+r.job_id);await refresh();
  });
});
el("predict-form").addEventListener("submit",e=>{
  e.preventDefault();action(async()=>{
    const f=new FormData();f.append("model_id",el("model-id").value);f.append("image",el("image").files[0]);
    const r=await call("/predictions",{method:"POST",body:f});
    el("result").textContent=JSON.stringify(r,null,2);notice("Inference complete.");
  });
});
fetch("/api/health").then(r=>r.json()).then(r=>el("health").textContent="API "+r.status).catch(()=>el("health").textContent="API unavailable");
call("/auth/session").then(r=>{csrf=r.csrf;return refresh();}).catch(()=>{});
