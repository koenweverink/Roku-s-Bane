import numpy as np


class Comet:
    
    def __init__(self, V_init: float, M_init: float, angle: int) -> None:
        
        # constants, nonmutable variables
        self.C_d: int = 1                   # Drag coefficient
        self.C_h: float = 0.15              # Heat transfer coefficient; backed by different source, max val
        self.Q: int = 3E6                   # Heat of ablation (J)
        self.density: int = 3500            # density of ordinary chondrite (kg/m^3)
        self.shape_factor: float = 1.2      # shape factor
        self.g: float = 9.81                # gravitational constant

        # experimental starting values
        self.angle: int = angle             # angle of entry
        self.V_init: int = V_init           # initial velocity (m/s)
        self.M_init: float = M_init         # initial mass (kg)

        # updating variables (with initial values)
        self.h: float = 2.0E5               # distance from the earth (m)
        self.m: float = M_init              # mass (kg)
        self.v: float = V_init              # velocity (m/s) 
        self.w: float = 0                   # distance traveled (m)


    def air_density(self) -> float: # fix dit
        """
        Calculates the air density at different heights (h)
        
        >>> x = Comet(15000, 100000, 30)
        >>> x.h = 3E5
        >>> x.air_density()
        5.365972601885816e-07
        
        >>> x = Comet(15000, 100000, 30)
        >>> x.h = 15000 
        >>> x.air_density()
        0.0015261813207342312
        
        >>> x = Comet(15000, 100000, 30) 
        >>> x.h = 1000
        >>> x.air_density()
        0.0017562828078283295
        """
        air_density = 1.3 * np.exp(-self.h / 7000)
        return air_density


    def change_in_velocity(self) -> float:
        """
        Calculates the acceleration of a meteor at a point in time, given:

        The drag coefficient (C_d), shape factor, air density,  
        velocity of the meteor (v), mass, density of the meteor,
        gravitation constant (g) and the angle of motion.

        Returns the acceleration (m/s^2)
        """
        dV_dt = -(self.C_d * self.shape_factor * self.air_density() * (self.v**2)) \
            / ((self.m**(1/3)) * self.density**(2/3)) + (self.g * np.cos(self.angle))
        return dV_dt


    def change_in_mass(self) -> float:
        """
        Calculates the rate of change in mass of the meteor at a point in time, given:

        The heat transfer coefficient (C_h), shape factor, air density,
        velocity of the meteor (v), mass, density of the meteor
        and the heat of ablation (Q)

        Returns the change in mass (kg/s)
        """
    
        dM_dt = -(self.C_h * self.shape_factor * self.air_density() * (self.v**3) \
            * ((self.m / self.density)**(2/3)) / (2 * self.Q))
        return dM_dt

if __name__ == "__main__":
    import doctest
    doctest.testmod()