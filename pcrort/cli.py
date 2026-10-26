"""PC-RORT command line entrypoint."""
from __future__ import annotations
import argparse
from importlib.metadata import version


def main() -> None:
    parser = argparse.ArgumentParser(prog="pcrort", description="PC-RORT experiments and tools")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("version", help="Print installed PC-RORT version")
    commands.add_parser("demo", help="Run the covariance-aware two-candidate example")
    commands.add_parser("web", help="Launch the local web portal (configure .env first)")
    args = parser.parse_args()
    if args.command == "version":
        print(version("pcrort"))
    elif args.command == "demo":
        import numpy as np
        from .matrix import two_candidate_robust_selection
        full = np.array([[1., 1.5], [1.5, 9.]])
        diag = np.diag([1., 9.])
        for name, matrix in (("shared-covariance", full), ("diagonal-ablation", diag)):
            fit = two_candidate_robust_selection(matrix, radius=0., rho=0.5)
            print(f"{name}: external_weight={fit.external_weight:.4f}, "
                  f"contrast={fit.robust_contrast:.4f}")
    else:
        try:
            import uvicorn
        except ImportError as exc:
            parser.error("Install optional portal dependencies with pip install -e '.[web]'")
            raise exc
        uvicorn.run("webapp.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
