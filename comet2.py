import numpy as np
from pyatmos import expo


class Comet:
    
    def __init__(self, V_init: float, M_init: float, angle: int) -> None:
        
        # constants, nonmutable variables
        self.C_d: float = 1                 # Drag coefficient
        self.C_h: float = 0.15              # Heat transfer coefficient; backed by different source, max val
        self.Q: int = 3E6                   # Heat of ablation (J)
        self.density: int = 3500            # density of ordinary chondrite (kg/m^3)
        self.shape_factor = 1.2             # shape factor
        self.g = 9.81                       # gravitational constant

        # experimental starting values
        self.angle = angle                  # angle of entry
        self.V_init = V_init                # initial velocity (m/s)
        self.M_init = M_init                # initial mass (kg)

        # updating variables (with initial values)
        self.h: float = 2.0E5               # distance from the earth (m)
        self.m = M_init                     # mass (kg)
        self.v = V_init                     # velocity (m/s) 
        self.x = 0                          # distance traveled (m)



    def radius(self) -> float:
        """
        Calculates the radius of the meteorite, based on the density and mass
        
        >>> x = Comet(15000, 100000, 30)
        >>> x.radius(100) > x.radius(1000)
        True
        >>> type(x.radius(10.112)) == np.float64 
        True
        >>> x.radius(10) == x.radius(10)
        True
        """
        mass = self.m * 1000

        value = (3 * mass) / (4 * self.density * np.pi)
        radius = np.cbrt(value)     # in cm
        radius = radius / 100       # in m
        # print(radius)
        return radius


    def projected_area(self) -> float:
        """ 
        Gives the 2d area of the 3d meteor that faces the direction of velocity,
        or in other words, the area undergoing most air pressure.
        
        >>> x = Comet(15000, 100000, 30)
        >>> x.projected_area(100.0) > x.projected_area(10.0)
        True
        >>> x = Comet(15000, 100000, 30)
        >>> type(x.projected_area(100.0)) == float
        True
        """
        return np.pi * self.radius()**2



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
        height = self.h
        air_density = 1.3 * np.exp(-height / 7000)
        return air_density


    def change_in_velocity(self):
        dV_dt = -(self.C_d * self.shape_factor * self.air_density() * (self.v**2)) / ((self.m**(1/3)) * self.density**(2/3)) + (self.g * np.cos(self.angle))
        return dV_dt


    def change_in_mass(self):
    #     dM_dt = -(self.C_h * self.shape_factor * self.air_density() * (self.v**3) * (self.m**(2/3))) / (2 * self.Q * self.density**(2/3))
    
        dM_dt = -(self.C_h * self.shape_factor * self.air_density() * (self.v**3) * ((self.m / self.density)**(2/3)) / (2 * self.Q))
        return dM_dt


    # Complex Formulas
    # def change_in_velocity(self) -> float:
    #     """
    #     Calculates the change in velocity over time of the meteorite
    #     """
    #     # dV_dt: float = -self.C_d * ((self.air_density() * self.projected_area() * \
    #     #     self.V_init**2) / self.m) + self.gravity() * np.sin(self.angle)

    #     dV_dt = (-(1/2) * (self.C_d * self.projected_area() * self.air_density() * (self.v**2)) / self.m) + (self.gravity() * np.sin(self.angle))
    #     return dV_dt


    # def change_in_temp(self) -> float:
    #     radius = self.radius() * 1000
    #     dT_dt = 1 / radius**2
    #     self.T += dT_dt * 0.001
    #     # print(self.T)
    #     return dT_dt
    

    # def change_in_mass(self) -> float:
    #     """
    #     Calculates the change in mass over time of the meteorite
    #     """
    #     # self.change_in_temp()
    #     # param1 = (self.C_h * self.air_density() * self.v**3) / 2
    #     # param2 = self.sigma * self.T**4

    #     # # # print(param1)
    #     # # # print(param2)

    #     # value = min(param1, param2)
    #     # # # print(value)

    #     # dM_dt = -self.projected_area() * (value / (self.M_init * self.Q))
    #     # # # dM_dt = -self.projected_area() * (value / (self.Q))
    #     # # # print(dM_dt)
    #     # return dM_dt

    #     dM_dt = -self.air_density() * self.projected_area() * (self.V_init) / (self.m * self.Q)
    #     return dM_dt



if __name__ == "__main__":
    import doctest
    doctest.testmod()