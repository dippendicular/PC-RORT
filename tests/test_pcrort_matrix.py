"""Small deterministic paper-equation regression tests; run with unittest."""
import unittest
import numpy as np
from pcrort.matrix import conditional_risk_matrix, relative_contrast, two_candidate_robust_selection


class TestPCRORTMatrix(unittest.TestCase):
    def test_joint_covariance_keeps_shared_encoder_block(self):
        # epsilon_local = Z, epsilon_source = 1.5 Z + eta; Var(eta)=6.75
        v = np.array([[1.0, 1.5], [1.5, 9.0]])
        q = conditional_risk_matrix(np.zeros((1, 2)), np.eye(1), v.reshape(2, 1, 2, 1))
        np.testing.assert_allclose(q, v)
        self.assertAlmostEqual(relative_contrast([1., 0.], q), 0.)
        self.assertAlmostEqual(relative_contrast([0.9, 0.1], q), 0.17)

    def test_covariance_include_exclude_flip(self):
        full = np.array([[1., 1.5], [1.5, 9.]])
        diagonal = np.diag(np.diag(full))
        f = two_candidate_robust_selection(full, 0., 0.5)
        d = two_candidate_robust_selection(diagonal, 0., 0.5)
        self.assertTrue(f.local_only)
        self.assertAlmostEqual(d.external_weight, 0.1, places=6)
        self.assertAlmostEqual(d.robust_contrast, -0.1, places=6)

    def test_positive_radius_power_threshold(self):
        diagonal = np.diag([1., 9.])
        self.assertFalse(two_candidate_robust_selection(diagonal, 0.2, 0.5).local_only)
        self.assertTrue(two_candidate_robust_selection(diagonal, 0.9, 0.5).local_only)

    def test_fail_closed_outside_supported_psd_geometry(self):
        with self.assertRaises(NotImplementedError):
            two_candidate_robust_selection(np.diag([1., 9.]), 1.2, 0.5)

    def test_non_psd_joint_covariance_rejected(self):
        with self.assertRaises(ValueError):
            conditional_risk_matrix(np.zeros((1, 2)), np.eye(1),
                                    np.array([[1., 2.], [2., 1.]]).reshape(2, 1, 2, 1))


if __name__ == "__main__":
    unittest.main()
