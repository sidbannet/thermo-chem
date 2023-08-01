# -*- coding: utf-8 -*-
"""
pmutt.test_pmutt_model_reaction_bep
Tests for pmutt module
"""
import unittest
from sycamore.physics._pmutt import constants as c
from sycamore.physics._pmutt.reaction import Reaction
from sycamore.physics._pmutt.reaction.bep import BEP
from sycamore.physics._pmutt.statmech import StatMech, presets


class TestBEP(unittest.TestCase):
    def setUp(self):
        self.T = c.T0('K')
        # Factor to convert potential energy to dimensionless number
        dim_factor = c.R('eV/K') * self.T
        self.m = 0.5  # BEP Slope
        self.c = 20.  # BEP Intercept in kcal/mol
        species = {
            'H2':
            StatMech(name='H2',
                     potentialenergy=2. * dim_factor,
                     **presets['electronic']),
            'O2':
            StatMech(name='O2',
                     potentialenergy=4. * dim_factor,
                     **presets['electronic']),
            'H2O':
            StatMech(name='H2O',
                     potentialenergy=3. * dim_factor,
                     **presets['electronic']),
            'BEP_delta_H':
            BEP(name='BEP_delta_H',
                slope=self.m,
                intercept=self.c,
                descriptor='delta_H'),
            'BEP_rev_delta_H':
            BEP(name='BEP_rev_delta_H',
                slope=self.m,
                intercept=self.c,
                descriptor='delta_H'),
            'BEP_reactants_H':
            BEP(name='BEP_rev_reactants_H',
                slope=self.m,
                intercept=self.c,
                descriptor='reactants_H'),
            'BEP_products_H':
            BEP(name='BEP_rev_products_H',
                slope=self.m,
                intercept=self.c,
                descriptor='products_H'),
            'BEP_delta_E':
            BEP(name='BEP_delta_E',
                slope=self.m,
                intercept=self.c,
                descriptor='delta_E'),
            'BEP_rev_delta_E':
            BEP(name='BEP_rev_delta_E',
                slope=self.m,
                intercept=self.c,
                descriptor='delta_E'),
            'BEP_reactants_E':
            BEP(name='BEP_rev_reactants_E',
                slope=self.m,
                intercept=self.c,
                descriptor='reactants_E'),
            'BEP_products_E':
            BEP(name='BEP_rev_products_E',
                slope=self.m,
                intercept=self.c,
                descriptor='products_E'),
        }
        self.rxn_delta_H = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_delta_H = H2O', species=species)
        self.bep_delta_H = self.rxn_delta_H.transition_state[0]

        rxn_rev_delta_H = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_rev_delta_H = H2O', species=species)
        self.bep_rev_delta_H = rxn_rev_delta_H.transition_state[0]

        rxn_reactants_H = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_reactants_H = H2O', species=species)
        self.bep_reactants_H = rxn_reactants_H.transition_state[0]

        rxn_products_H = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_products_H = H2O', species=species)
        self.bep_products_H = rxn_products_H.transition_state[0]

        self.rxn_delta_E = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_delta_E = H2O', species=species)
        self.bep_delta_E = self.rxn_delta_E.transition_state[0]

        rxn_rev_delta_E = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_rev_delta_E = H2O', species=species)
        self.bep_rev_delta_E = rxn_rev_delta_E.transition_state[0]

        rxn_reactants_E = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_reactants_E = H2O', species=species)
        self.bep_reactants_E = rxn_reactants_E.transition_state[0]

        rxn_products_E = Reaction.from_string(
            reaction_str='H2 + 0.5O2 = BEP_products_E = H2O', species=species)
        self.bep_products_E = rxn_products_E.transition_state[0]

    def test_get_EoRT(self):
        # This should be separated into multiple tests at some point.
        delta_H = self.rxn_delta_H.get_delta_HoRT(T=self.T)
        exp_EoRT_delta = self.m * delta_H + self.c / c.R('kcal/mol/K') / self.T
        exp_EoRT_delta_rev = (self.m-1.)*delta_H \
                             + self.c/c.R('kcal/mol/K')/self.T
        self.assertAlmostEqual(
            self.bep_delta_H.get_EoRT_act(T=self.T,
                                          rev=False,
                                          reaction=self.rxn_delta_H),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_delta_H.get_EoRT_act(T=self.T,
                                          rev=True,
                                          reaction=self.rxn_delta_H),
            exp_EoRT_delta_rev)

        rev_delta_H = self.rxn_delta_H.get_delta_HoRT(T=self.T, rev=True)
        exp_EoRT_delta = (self.m-1.)*rev_delta_H \
                         + self.c/c.R('kcal/mol/K')/self.T
        exp_EoRT_delta_rev = self.m*rev_delta_H \
                             + self.c/c.R('kcal/mol/K')/self.T
        self.assertAlmostEqual(
            self.bep_rev_delta_H.get_EoRT_act(T=self.T,
                                              rev=False,
                                              reaction=self.rxn_delta_H),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_rev_delta_H.get_EoRT_act(T=self.T,
                                              rev=True,
                                              reaction=self.rxn_delta_H),
            exp_EoRT_delta_rev)

        reactants_H = self.rxn_delta_H.get_HoRT_state(state='reactants',
                                                      T=self.T)
        exp_EoRT_delta = self.m * reactants_H + self.c / c.R(
            'kcal/mol/K') / self.T
        exp_EoRT_delta_rev = (self.m-1.)*reactants_H \
                             + self.c/c.R('kcal/mol/K')/self.T

        self.assertAlmostEqual(
            self.bep_reactants_H.get_EoRT_act(T=self.T,
                                              rev=False,
                                              reaction=self.rxn_delta_H),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_reactants_H.get_EoRT_act(T=self.T,
                                              rev=True,
                                              reaction=self.rxn_delta_H),
            exp_EoRT_delta_rev)

        products_H = self.rxn_delta_H.get_HoRT_state(state='products',
                                                     T=self.T)
        exp_EoRT_delta = self.m * products_H + self.c / c.R(
            'kcal/mol/K') / self.T
        exp_EoRT_delta_rev = (self.m-1.)*products_H \
                             + self.c/c.R('kcal/mol/K')/self.T

        self.assertAlmostEqual(
            self.bep_products_H.get_EoRT_act(T=self.T,
                                             rev=False,
                                             reaction=self.rxn_delta_H),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_products_H.get_EoRT_act(T=self.T,
                                             rev=True,
                                             reaction=self.rxn_delta_H),
            exp_EoRT_delta_rev)

        delta_E = self.rxn_delta_E.get_delta_EoRT(T=self.T)
        exp_EoRT_delta = self.m * delta_E + self.c / c.R('kcal/mol/K') / self.T
        exp_EoRT_delta_rev = (self.m-1.)*delta_E \
                             + self.c/c.R('kcal/mol/K')/self.T

        self.assertAlmostEqual(
            self.bep_delta_E.get_EoRT_act(T=self.T,
                                          rev=False,
                                          reaction=self.rxn_delta_E),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_delta_E.get_EoRT_act(T=self.T,
                                          rev=True,
                                          reaction=self.rxn_delta_E),
            exp_EoRT_delta_rev)

        rev_delta_E = self.rxn_delta_E.get_delta_EoRT(T=self.T, rev=True)
        exp_EoRT_delta = (self.m-1.)*rev_delta_E \
                         + self.c/c.R('kcal/mol/K')/self.T
        exp_EoRT_delta_rev = self.m*rev_delta_E \
                             + self.c/c.R('kcal/mol/K')/self.T

        self.assertAlmostEqual(
            self.bep_rev_delta_E.get_EoRT_act(T=self.T,
                                              rev=False,
                                              reaction=self.rxn_delta_E),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_rev_delta_E.get_EoRT_act(T=self.T,
                                              rev=True,
                                              reaction=self.rxn_delta_E),
            exp_EoRT_delta_rev)

        reactants_E = self.rxn_delta_E.get_EoRT_state(state='reactants',
                                                      T=self.T)
        exp_EoRT_delta = self.m * reactants_E + self.c / c.R(
            'kcal/mol/K') / self.T
        exp_EoRT_delta_rev = (self.m-1.)*reactants_E \
                             + self.c/c.R('kcal/mol/K')/self.T

        self.assertAlmostEqual(
            self.bep_reactants_E.get_EoRT_act(T=self.T,
                                              rev=False,
                                              reaction=self.rxn_delta_E),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_reactants_E.get_EoRT_act(T=self.T,
                                              rev=True,
                                              reaction=self.rxn_delta_E),
            exp_EoRT_delta_rev)

        products_E = self.rxn_delta_E.get_EoRT_state(state='products',
                                                     T=self.T)
        exp_EoRT_delta = self.m * products_E + self.c / c.R(
            'kcal/mol/K') / self.T
        exp_EoRT_delta_rev = (self.m-1.)*products_E \
                             + self.c/c.R('kcal/mol/K')/self.T

        self.assertAlmostEqual(
            self.bep_products_E.get_EoRT_act(T=self.T,
                                             rev=False,
                                             reaction=self.rxn_delta_E),
            exp_EoRT_delta)
        self.assertAlmostEqual(
            self.bep_products_E.get_EoRT_act(T=self.T,
                                             rev=True,
                                             reaction=self.rxn_delta_E),
            exp_EoRT_delta_rev)


if __name__ == '__main__':
    unittest.main()
