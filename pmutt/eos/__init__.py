# -*- coding: utf-8 -*-
"""
pmutt.eos
Vlachos group code to model equations of state.
Created on Tues Jul 10 12:40:00 2018
"""

import numpy as np

from sycamore.physics._pmutt import _pmuttBase
from sycamore.physics._pmutt import constants as c
from sycamore.physics._pmutt.io.json import remove_class


class IdealGasEOS(_pmuttBase):
    """Ideal gas equation of state

    :math:`PV=nRT`
    """
    def __init__(self):
        # Ideal gas does not have any attributes!
        pass

    def get_V(self, T=c.T0('K'), P=c.P0('bar'), n=1.):
        """Calculates the volume of an ideal gas

        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is standard temperature
            P : float, optional
                Pressure in bar. Default is standard pressure
            n : float, optional
                Number of moles (in mol). Default is 1 mol
        Returns
        -------
            V : float
                Volume in m3
        """
        return n * c.R('m3 bar/mol/K') * T / P

    def get_P(self, T=c.T0('K'), V=c.V0('m3'), n=1.):
        """Calculates the pressure of an ideal gas

        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is standard temperature
            V : float, optional
                Volume in m3. Default is standard volume
            n : float, optional
                Number of moles (in mol). Default is 1 mol
        Returns
        -------
            P : float
                Pressure in bar
        """
        return n * c.R('m3 bar/mol/K') * T / V

    def get_T(self, V=c.V0('m3'), P=c.P0('bar'), n=1.):
        """Calculates the temperature of an ideal gas

        Parameters
        ----------
            V : float, optional
                Volume in m3. Default is standard volume
            P : float, optional
                Pressure in bar. Default is standard pressure
            n : float, optional
                Number of moles (in mol). Default is 1 mol
        Returns
        -------
            T : float
                Temperature in K
        """
        return P * V / c.R('m3 bar/mol/K') / n

    def get_n(self, V=c.V0('m3'), P=c.P0('bar'), T=c.T0('K')):
        """Calculates the moles of an ideal gas

        Parameters
        ----------
            V : float, optional
                Volume in m3. Default is standard volume
            P : float, optional
                Pressure in bar. Default is standard pressure
            T : float, optional
                Temperature in K. Default is standard temperature
        Returns
        -------
            n : float
                Number of moles in mol
        """
        return P * V / c.R('m3 bar/mol/K') / T


class vanDerWaalsEOS(_pmuttBase):
    """van der Waals equation of state

    :math:`\\bigg(P+a\\big(\\frac{n}{V}\\big)^2 \\bigg)\\bigg(\\frac{V}{n}-b
    \\bigg)=RT`

    Attributes
    ----------
        a : float
            Measure of average attraction between particles in Pa m6/mol
        b : float
            Volume excluded by a mole of particles in m3/mol
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_Vm(self, T=c.T0('K'), P=c.P0('bar'), gas_phase=True):
        """Calculates the molar volume of a van der Waals gas

        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is standard temperature
            P : float, optional
                Pressure in bar. Default is standard pressure
            gas_phase : bool, optional
                Relevant if system is in vapor-liquid equilibrium. If True,
                return the larger volume (gas phase). If False, returns the
                smaller volume (liquid phase).
        Returns
        -------
            Vm : float
                Volume in m3
        """
        P_SI = P * c.convert_unit(initial='bar', final='Pa')
        Vm = np.roots([
            P_SI, -(P_SI * self.b + c.R('J/mol/K') * T), self.a,
            -self.a * self.b
        ])
        real_Vm = np.real([Vm_i for Vm_i in Vm if np.isreal(Vm_i)])
        if gas_phase:
            return np.max(real_Vm)
        else:
            return np.min(real_Vm)

    def get_V(self, T=c.T0('K'), P=c.P0('bar'), n=1., gas_phase=True):
        """Calculates the volume of a van der Waals gas

        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is standard temperature
            P : float, optional
                Pressure in bar. Default is standard pressure
            n : float, optional
                Number of moles (in mol). Default is 1 mol
            gas_phase : bool, optional
                Relevant if system is in vapor-liquid equilibrium. If True,
                return the larger volume (gas phase). If False, returns the
                smaller volume (liquid phase).
        Returns
        -------
            V : float
                Volume in m3
        """
        return self.get_Vm(T=T, P=P, gas_phase=gas_phase) * n

    def get_P(self, T=c.T0('K'), V=c.V0('m3'), n=1.):
        """Calculates the pressure of a van der Waals gas

        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is standard temperature
            V : float, optional
                Volume in m3. Default is standard volume
            n : float, optional
                Number of moles (in mol). Default is 1 mol
        Returns
        -------
            P : float
                Pressure in bar
        """
        Vm = V / n
        return (c.R('J/mol/K')*T/(Vm - self.b) - self.a*(1./Vm)**2) \
            * c.convert_unit(initial='Pa', final='bar')

    def get_T(self, V=c.V0('m3'), P=c.P0('bar'), n=1.):
        """Calculates the temperature of a van der Waals gas

        Parameters
        ----------
            V : float, optional
                Volume in m3. Default is standard volume
            P : float, optional
                Pressure in bar. Default is standard pressure
            n : float, optional
                Number of moles (in mol). Default is 1 mol
        Returns
        -------
            T : float
                Temperature in K
        """
        Vm = V / n
        return (P*c.convert_unit(initial='bar', final='Pa') + self.a/Vm**2) \
            * (Vm - self.b)/c.R('J/mol/K')

    def get_n(self, V=c.V0('m3'), P=c.P0('bar'), T=c.T0('K'), gas_phase=True):
        """Calculates the moles of a van der Waals gas

        Parameters
        ----------
            V : float, optional
                Volume in m3. Default is standard volume
            P : float, optional
                Pressure in bar. Default is standard pressure
            T : float, optional
                Temperature in K. Default is standard temperature
            gas_phase : bool, optional
                Relevant if system is in vapor-liquid equilibrium. If True,
                return the smaller moles (gas phase). If False, returns the
                larger moles (liquid phase).
        Returns
        -------
            n : float
                Number of moles in mol
        """
        return V / self.get_Vm(T=T, P=P, gas_phase=gas_phase)

    def get_Pc(self):
        """Calculates the critical pressure

        Returns
        -------
            Pc : float
                Critical pressure in bar
        """
        return self.a / 27. / self.b**2 * c.convert_unit(initial='Pa',
                                                         final='bar')

    def get_Tc(self):
        """Calculates the critical temperature

        Returns
        -------
            Tc : float
                Critcial temperature in K
        """
        return 8. * self.a / 27. / self.b / c.R('J/mol/K')

    def get_Vc(self, n=1.):
        """Calculates the critical volume

        Parameters
        ----------
            n : float, optional
                Number of moles in mol. Default is 1 mol
        Returns
        -------
            Vc : float
                Critical volume in m3
        """
        return 3. * n * self.b

    @classmethod
    def from_critical(cls, Tc, Pc):
        """Creates the van der Waals object from critical temperature and
        pressure

        Parameters
        ----------
            Tc : float
                Critical temperature in K
            Pc : float
                Critical pressure in bar
        Returns
        -------
            vanDerWaalsEOS : vanDerWaalsEOS object
        """
        Pc_SI = Pc * c.convert_unit(initial='bar', final='Pa')
        a = 27. / 64. * (c.R('J/mol/K') * Tc)**2 / Pc_SI
        b = c.R('J/mol/K') * Tc / 8. / Pc_SI
        return cls(a=a, b=b)
