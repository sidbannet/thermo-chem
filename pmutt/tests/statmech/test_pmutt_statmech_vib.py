# -*- coding: utf-8 -*-
"""
pmutt.test_pmutt_model_statmech_vib
Tests for pmutt module
"""
import unittest
import numpy as np
from sycamore.physics.pmutt import constants as c
from sycamore.physics.pmutt.statmech import vib


class TestHarmonicVib(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.vib_H2 = vib.HarmonicVib(vib_wavenumbers=[4306.1793])
        self.vib_H2O = vib.HarmonicVib(
            vib_wavenumbers=[3825.434, 3710.2642, 1582.432])
        self.vib_H2O_dict = {
            'class': "<class 'pmutt.statmech.vib.HarmonicVib'>",
            'vib_wavenumbers': [3825.434, 3710.2642, 1582.432],
            'imaginary_substitute': None
        }
        self.T = 300.  # K

    def test_get_q(self):
        self.assertAlmostEqual(self.vib_H2.get_q(T=self.T), 3.27680884e-05)
        self.assertAlmostEqual(self.vib_H2O.get_q(T=self.T), 3.1464834E-10)

    def test_get_CvoR(self):
        self.assertAlmostEqual(self.vib_H2.get_CvoR(T=self.T), 4.52088E-07)
        self.assertAlmostEqual(self.vib_H2O.get_CvoR(T=self.T), 0.02917545)

    def test_get_CpoR(self):
        self.assertAlmostEqual(self.vib_H2.get_CpoR(T=self.T), 4.52088E-07)
        self.assertAlmostEqual(self.vib_H2O.get_CpoR(T=self.T), 0.02917545)

    def test_get_ZPE(self):
        self.assertAlmostEqual(self.vib_H2.get_ZPE(), 0.26694909102484027)
        self.assertAlmostEqual(self.vib_H2O.get_ZPE(), 0.5652520248602153)

    def test_get_UoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_UoRT(T=self.T), 10.32605545)
        self.assertAlmostEqual(self.vib_H2O.get_UoRT(T=self.T), 21.8687737)

    def test_get_HoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_HoRT(T=self.T), 10.32605545)
        self.assertAlmostEqual(self.vib_H2O.get_HoRT(T=self.T), 21.8687737)

    def test_get_SoR(self):
        self.assertAlmostEqual(self.vib_H2.get_SoR(T=self.T),
                               2.32489026469e-08)
        self.assertAlmostEqual(self.vib_H2O.get_SoR(T=self.T), 0.00434769)

    def test_get_FoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_FoRT(T=self.T), 1.032605543E+01)
        self.assertAlmostEqual(self.vib_H2O.get_FoRT(T=self.T),
                               2.186442601E+01)

    def test_get_GoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_GoRT(T=self.T), 1.032605543E+01)
        self.assertAlmostEqual(self.vib_H2O.get_GoRT(T=self.T),
                               2.186442601E+01)

    def test_to_dict(self):
        self.assertEqual(self.vib_H2O.to_dict(), self.vib_H2O_dict)

    def test_from_dict(self):
        self.assertEqual(vib.HarmonicVib.from_dict(self.vib_H2O_dict),
                         self.vib_H2O)


class TestQRRHOVib(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.vib_H2 = vib.QRRHOVib(vib_wavenumbers=[4306.1793])
        self.vib_H2O = vib.QRRHOVib(
            vib_wavenumbers=[3825.434, 3710.2642, 1582.432])
        self.vib_H2O_dict = {
            'class': "<class 'pmutt.statmech.vib.QRRHOVib'>",
            'vib_wavenumbers': [3825.434, 3710.2642, 1582.432],
            'alpha': 4,
            'Bav': 1.e-44,
            'v0': 100,
            'imaginary_substitute': None
        }
        self.T = 300.  # K

    def test_get_scaled_wavenumber(self):
        np.testing.assert_array_almost_equal(
            np.array(
                [9.999995330429E-01, 9.999994723081E-01, 9.999840524913E-01]),
            self.vib_H2O._get_scaled_wavenumber())

    def test_get_scaled_inertia(self):
        np.testing.assert_array_almost_equal(
            np.array(
                [7.317482550162E-50, 7.544621804437E-50, 1.768938962532E-49]),
            self.vib_H2O._get_scaled_inertia())

    def test_get_CvoR(self):
        self.assertAlmostEqual(self.vib_H2.get_CvoR(T=self.T),
                               6.0337598762E-07)
        self.assertAlmostEqual(self.vib_H2O.get_CvoR(T=self.T),
                               2.918349716E-02)

    def test_get_CpoR(self):
        self.assertAlmostEqual(self.vib_H2.get_CpoR(T=self.T),
                               6.0337598762E-07)
        self.assertAlmostEqual(self.vib_H2O.get_CpoR(T=self.T),
                               2.918349716E-02)

    def test_get_UoRT_RHHO(self):
        self.assertAlmostEqual(
            self.vib_H2O._get_UoRT_RRHO(T=self.T, vib_temperature=2276.767335),
            3.798453353623928)

    def test_get_UoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_UoRT(T=self.T),
                               10.3260525951174)
        self.assertAlmostEqual(self.vib_H2O.get_UoRT(T=self.T),
                               21.868712644411)

    def test_get_HoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_UoRT(T=self.T),
                               10.3260525951174)
        self.assertAlmostEqual(self.vib_H2O.get_HoRT(T=self.T),
                               21.868712644411)

    def test_get_SoR_H(self):
        self.assertAlmostEqual(
            self.vib_H2O._get_SoR_H(T=self.T, vib_temperature=2276.767335),
            0.0043471298500)

    def test_get_SoR_RRHO(self):
        self.assertAlmostEqual(
            self.vib_H2O._get_SoR_RRHO(T=self.T, vib_inertia=1.768938963E-49),
            5.899139738E-02)

    def test_get_SoR(self):
        # It's odd that this evaluated to a negative quantity. However, this
        # may be due to qRRHO not being valid for species with more
        # harmonic-like vibrations?
        self.assertAlmostEqual(self.vib_H2.get_SoR(T=self.T),
                               -1.0516394390905423e-07)
        self.assertAlmostEqual(self.vib_H2O.get_SoR(T=self.T),
                               0.004348189190084936)

    def test_get_FoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_FoRT(T=self.T),
                               10.326052700281332)
        self.assertAlmostEqual(self.vib_H2O.get_FoRT(T=self.T),
                               21.86436445522042)

    def test_get_GoRT(self):
        self.assertAlmostEqual(self.vib_H2.get_GoRT(T=self.T),
                               10.326052700281332)
        self.assertAlmostEqual(self.vib_H2O.get_GoRT(T=self.T),
                               21.86436445522042)

    def test_to_dict(self):
        self.assertEqual(self.vib_H2O.to_dict(), self.vib_H2O_dict)

    def test_from_dict(self):
        self.assertEqual(vib.QRRHOVib.from_dict(self.vib_H2O_dict),
                         self.vib_H2O)


class TestEinsteinVib(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.vib_Ag = vib.EinsteinVib(einstein_temperature=173.28913505677,
                                      interaction_energy=0.5)
        self.vib_Ag_dict = {
            'class': "<class 'pmutt.statmech.vib.EinsteinVib'>",
            'einstein_temperature': 173.28913505677,
            'interaction_energy': 0.5
        }
        self.T = 300.  # K

    def test_get_q(self):
        self.assertAlmostEqual(self.vib_Ag.get_q(T=self.T), 6.8029252699e-09)

    def test_get_CvoR(self):
        self.assertAlmostEqual(self.vib_Ag.get_CvoR(T=self.T), 2.9179591404057)

    def test_get_CpoR(self):
        self.assertAlmostEqual(self.vib_Ag.get_CpoR(T=self.T), 2.9179591404057)

    def test_get_ZPE(self):
        self.assertAlmostEqual(self.vib_Ag.get_ZPE(), 0.5223993457128)

    def test_get_UoRT(self):
        self.assertAlmostEqual(self.vib_Ag.get_UoRT(T=self.T),
                               22.4238242106867)

    def test_get_HoRT(self):
        self.assertAlmostEqual(self.vib_Ag.get_HoRT(T=self.T),
                               22.4238242106867)

    def test_get_SoR(self):
        self.assertAlmostEqual(self.vib_Ag.get_SoR(T=self.T), 4.6878251875495)

    def test_get_FoRT(self):
        self.assertAlmostEqual(self.vib_Ag.get_FoRT(T=self.T),
                               17.7359990231372)

    def test_get_GoRT(self):
        self.assertAlmostEqual(self.vib_Ag.get_GoRT(T=self.T),
                               17.7359990231372)

    def test_to_dict(self):
        self.assertEqual(self.vib_Ag.to_dict(), self.vib_Ag_dict)

    def test_from_dict(self):
        self.assertEqual(vib.EinsteinVib.from_dict(self.vib_Ag_dict),
                         self.vib_Ag)


class TestDebyeVib(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.theta_D = 215.
        self.u = 0.5
        self.vib_Ag = vib.DebyeVib(debye_temperature=self.theta_D,
                                   interaction_energy=self.u)
        self.vib_Ag_dict = {
            'class': "<class 'pmutt.statmech.vib.DebyeVib'>",
            'debye_temperature': self.theta_D,
            'interaction_energy': self.u
        }
        self.T = 300.  # K
        # Integrals calculated using Wolfram Alpha
        # https://www.wolframalpha.com/input/?i=integrate+x%5E3+exp(x)%2F(exp(x)-1)+dx+from+0+to+215%2F300
        self.F = 3. * (self.T / self.theta_D)**3 * 0.158802
        # https://www.wolframalpha.com/input/?i=integrate+x%5E2+*+ln(1-exp(-x))+dx+from+0+to+215%2F300
        self.G = 3. * (self.T / self.theta_D)**3 * -0.113178
        # https://www.wolframalpha.com/input/?i=integrate+x%5E4+exp(x)%2F(exp(x)-1)%5E2+dx+from+0+to+215%2F300
        self.K = 3. * (self.T / self.theta_D)**3 * 0.119602

    def test_get_q(self):
        exp_q = np.exp(-self.u/3./c.kb('eV/K')/self.T \
                       -3./8.*self.theta_D/self.T \
                       -self.G)
        self.assertAlmostEqual(self.vib_Ag.get_q(T=self.T), exp_q)

    def test_get_CvoR(self):
        self.assertAlmostEqual(self.vib_Ag.get_CvoR(T=self.T), 3. * self.K, 6)

    def test_get_CpoR(self):
        self.assertAlmostEqual(self.vib_Ag.get_CpoR(T=self.T), 3. * self.K, 6)

    def test_get_ZPE(self):
        self.assertAlmostEqual(self.vib_Ag.get_ZPE(),
                               self.u + 9. / 8. * self.theta_D * c.kb('eV/K'))

    def test_get_UoRT(self):
        exp_UoRT = (self.u + 9./8.*self.theta_D*c.kb('eV/K')) \
                   /c.kb('eV/K')/self.T \
                   + 3.*self.F
        self.assertAlmostEqual(self.vib_Ag.get_UoRT(T=self.T), exp_UoRT, 4)

    def test_get_HoRT(self):
        exp_HoRT = (self.u + 9./8.*self.theta_D*c.kb('eV/K')) \
                   /c.kb('eV/K')/self.T \
                   + 3.*self.F
        self.assertAlmostEqual(self.vib_Ag.get_HoRT(T=self.T), exp_HoRT, 4)

    def test_get_SoR(self):
        self.assertAlmostEqual(self.vib_Ag.get_SoR(T=self.T),
                               3. * (self.F - self.G), 4)

    def test_get_FoRT(self):
        exp_FoRT = self.vib_Ag.get_UoRT(T=self.T) - self.vib_Ag.get_SoR(
            T=self.T)
        self.assertAlmostEqual(self.vib_Ag.get_FoRT(T=self.T), exp_FoRT, 6)

    def test_get_GoRT(self):
        exp_GoRT = self.vib_Ag.get_HoRT(T=self.T) - self.vib_Ag.get_SoR(
            T=self.T)
        self.assertAlmostEqual(self.vib_Ag.get_GoRT(T=self.T), exp_GoRT, 6)

    def test_to_dict(self):
        self.assertEqual(self.vib_Ag.to_dict(), self.vib_Ag_dict)

    def test_from_dict(self):
        self.assertEqual(vib.DebyeVib.from_dict(self.vib_Ag_dict), self.vib_Ag)


if __name__ == '__main__':
    unittest.main()
