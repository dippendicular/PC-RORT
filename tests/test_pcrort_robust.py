"""General-J numerical regression tests, including covariance-decision flip."""
import unittest
import numpy as np
from pcrort.robust import UncertaintySet, separation_oracle, robust_select
from pcrort.uncertainty import pilot_risk_matrix, bootstrap_matrices, proposals, contains


class TestRobust(unittest.TestCase):
    def test_local_vertex_is_zero_for_all_oracles(self):
        center = np.array([[1., 1.5], [1.5, 9.]])
        local = np.array([1., 0.])
        for uncertainty in (
            UncertaintySet(center, "frobenius", .1),
            UncertaintySet(center, "box_psd", widths=np.full((2, 2), .1)),
            UncertaintySet(center, "affine_psd", .2,
                           directions=np.eye(2)[None, :, :]),
        ):
            worst = separation_oracle(local, uncertainty)
            self.assertAlmostEqual(worst.worst_case_value, 0., places=5)

    def test_general_j_selection_is_feasible(self):
        q = np.diag([2., 1., 3.])
        result = robust_select(UncertaintySet(q, "frobenius", 0.02), .5)
        self.assertTrue(result.converged)
        self.assertGreater(result.weights[1], 0)
        self.assertGreaterEqual(result.weights[0], .5 - 1e-5)
        self.assertLess(result.objective, 0.)
        self.assertLess(result.gap, 1e-4)

    def test_full_covariance_flip_with_robust_ball(self):
        full = np.array([[1., 1.5], [1.5, 9.]])
        diagonal = np.diag([1., 9.])
        radius = .1
        a = robust_select(UncertaintySet(full, "frobenius", radius), .5)
        b = robust_select(UncertaintySet(diagonal, "frobenius", radius), .5)
        self.assertLess(1 - a.weights[0], 1e-3)
        self.assertGreater(1 - b.weights[0], .01)

    def test_all_regions_contain_center(self):
        rng = np.random.default_rng(21)
        x = rng.normal(size=(30, 3, 2))
        q = pilot_risk_matrix(x, 20)
        bs = bootstrap_matrices(x, 20, 30, rng)
        for region in proposals(q, bs).values():
            self.assertTrue(contains(region, q))

    def test_non_psd_center_is_rejected(self):
        with self.assertRaises(ValueError):
            UncertaintySet(np.array([[1., 3.], [3., 1.]]), "frobenius", .1)


if __name__ == "__main__":
    unittest.main()
