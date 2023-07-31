# -*- coding: utf-8 -*-
"""
pmutt.test_pmutt_model_statmech_elec
Tests for pmutt module
"""
import unittest
import numpy as np
from sycamore.physics.pmutt.statmech import elec


class TestGroundStateElec(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.elec_H2 = elec.GroundStateElec(potentialenergy=-6.759576, spin=0.)
        self.elec_OH = elec.GroundStateElec(potentialenergy=-7.554949,
                                            spin=0.5)
        self.elec_O2 = elec.GroundStateElec(potentialenergy=-9.862407, spin=1.)
        self.elec_O2_dict = {
            'class': "<class 'pmutt.statmech.elec.GroundStateElec'>",
            'potentialenergy': -9.862407,
            'spin': 1.
        }

        self.T = 300  # K

    def test_get_q(self):
        # Using np.isclose instead of self.assertAlmostEqual since the latter
        # does not compare large floats very well
        self.assertTrue(
            np.isclose(self.elec_H2.get_q(T=self.T, ignore_q_elec=False),
                       3.5968135E+113))
        self.assertTrue(
            np.isclose(self.elec_OH.get_q(T=self.T, ignore_q_elec=False),
                       1.6543631E+127))
        self.assertTrue(
            np.isclose(self.elec_O2.get_q(T=self.T, ignore_q_elec=False),
                       1.4398714E+166))

        self.assertTrue(
            np.isclose(self.elec_H2.get_q(T=self.T, ignore_q_elec=True), 1.))
        self.assertTrue(
            np.isclose(self.elec_OH.get_q(T=self.T, ignore_q_elec=True), 1.))
        self.assertTrue(
            np.isclose(self.elec_O2.get_q(T=self.T, ignore_q_elec=True), 1.))

    def test_get_CvoR(self):
        self.assertEqual(self.elec_H2.get_CvoR(), 0.)
        self.assertEqual(self.elec_OH.get_CvoR(), 0.)
        self.assertEqual(self.elec_O2.get_CvoR(), 0.)

    def test_get_CpoR(self):
        self.assertEqual(self.elec_H2.get_CpoR(), 0.)
        self.assertEqual(self.elec_OH.get_CpoR(), 0.)
        self.assertEqual(self.elec_O2.get_CpoR(), 0.)

    def test_get_UoRT(self):
        self.assertTrue(
            np.isclose(self.elec_H2.get_UoRT(T=self.T), -2.614722E+02))
        self.assertTrue(
            np.isclose(self.elec_OH.get_UoRT(T=self.T), -2.922386E+02))
        self.assertTrue(
            np.isclose(self.elec_O2.get_UoRT(T=self.T), -3.814951E+02))

    def test_get_HoRT(self):
        self.assertTrue(
            np.isclose(self.elec_H2.get_HoRT(T=self.T), -2.614722E+02))
        self.assertTrue(
            np.isclose(self.elec_OH.get_HoRT(T=self.T), -2.922386E+02))
        self.assertTrue(
            np.isclose(self.elec_O2.get_HoRT(T=self.T), -3.814951E+02))

    def test_get_SoR(self):
        self.assertAlmostEqual(self.elec_H2.get_SoR(), np.log(1.))
        self.assertAlmostEqual(self.elec_OH.get_SoR(), np.log(2.))
        self.assertAlmostEqual(self.elec_O2.get_SoR(), np.log(3.))

    def test_get_FoRT(self):
        self.assertTrue(
            np.isclose(self.elec_H2.get_FoRT(T=self.T), -2.614722E+02))
        self.assertTrue(
            np.isclose(self.elec_OH.get_FoRT(T=self.T), -2.929317E+02))
        self.assertTrue(
            np.isclose(self.elec_O2.get_FoRT(T=self.T), -3.825937E+02))

    def test_get_GoRT(self):
        self.assertTrue(
            np.isclose(self.elec_H2.get_FoRT(T=self.T), -2.614722E+02))
        self.assertTrue(
            np.isclose(self.elec_OH.get_FoRT(T=self.T), -2.929317E+02))
        self.assertTrue(
            np.isclose(self.elec_O2.get_FoRT(T=self.T), -3.825937E+02))

    def test_to_dict(self):
        self.assertEqual(self.elec_O2.to_dict(), self.elec_O2_dict)

    def test_from_dict(self):
        self.assertEqual(elec.GroundStateElec.from_dict(self.elec_O2_dict),
                         self.elec_O2)


if __name__ == '__main__':
    unittest.main()
