"""Installation, notebook and package interface smoke checks."""
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestPCROTInterfaces(unittest.TestCase):
    def test_imports(self):
        from pcrort import conditional_risk_matrix, relative_contrast
        from pcrort.robust import UncertaintySet, robust_select
        self.assertTrue(callable(conditional_risk_matrix))
        self.assertTrue(callable(relative_contrast))
        self.assertTrue(callable(robust_select))

    def test_demo_cli(self):
        process = subprocess.run(
            [sys.executable, "-m", "pcrort.cli", "demo"],
            cwd=ROOT, text=True, capture_output=True, check=True
        )
        self.assertIn("shared-covariance", process.stdout)
        self.assertIn("diagonal-ablation", process.stdout)

    def test_notebook_is_valid(self):
        notebook = json.loads((ROOT / "notebooks" / "run_pipeline.ipynb").read_text())
        self.assertEqual(notebook["nbformat"], 4)
        self.assertTrue(any(c.get("cell_type") == "code" for c in notebook["cells"]))


if __name__ == "__main__":
    unittest.main()
