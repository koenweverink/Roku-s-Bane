import numpy as np
from pyatmos import expo

class Comet:
    
    def __init__(self, V_init: float, M_init: float, angle: int) -> None:
        
        # constants, nonmutable variables
        self.R: float = 6371000         # Radius of the Earth (m) 
        self.C_d: float = 0.47          # Drag coefficient
        self.C_h: float = 0.045         # Heat transfer coefficient; backed by different source, max val
        self.sigma: float = 5.6697E-8   # Stefan-Boltzmann constant       
        self.Q: int = 8.26E6            # Heat of ablation (J)  -> J of MJ???
        self.g: float = 9.81            # gravitational constant (m/s^2)
        self.total_height: float = 2E5  # initial height (m)
        self.density: int = 3.5         # density of ordinary chondrite (g/cm^3)

        # experimental starting values
        self.angle = angle      # angle of entry
        self.V_init = V_init    # initial velocity (m/s)
        self.M_init = M_init    # initial mass (kg)

        # updating variables (with initial values)
        self.h: float = 2E5             # distance from the earth (m)
        self.m: float = M_init          # mass (kg)
        self.v: float = V_init          # velocity (m/s) 
        self.x: float = 0               # distance traveled (m)
        self.T: float = 2073.2          # Temperature (K)   ->  iffy opzoeken

        

    # Simple Formulas
    def gravity(self) -> float:
        """
        Calculates the gravitation constant at the height of the comet above the earth
        >>> x, y = Comet(15000, 100000, 30), Comet(15000, 100000, 30)
        >>> x.h, y.h = 100, 1000
        >>> x.gravity() > y.gravity()
        True

        >>> x = Comet(15000, 100000, 30)
        >>> x.h = 3
        >>> x.gravity() == 9.81 * (1 - 6/x.R)
        True

        >>> x = Comet(15000, 100000, 30)
        >>> x.h = 500
        >>> type(x.gravity()) == float
        True
        """

        if self.h != 0:
            g = self.g * (1 - (2 * self.h / self.R))
        return g


    def weight(self) -> float:
        """
        Calculates the weight of the comet
        >>> x, y = Comet(15000, 100000, 30), Comet(15000, 10000, 30)
        >>> y.weight() < x.weight()
        True
        
        >>> x = Comet(15000, 100000, 30)
        >>> type(x.weight()) == float
        True
        """
        return self.m * self.gravity()


    def radius(self) -> float:
        """
        Calculates the radius of the meteorite, based on the density and mass

        """
        mass = self.m * 1000

        value = (3 * mass) / (4 * self.density * np.pi)
        radius = np.cbrt(value)     # in cm
        radius = radius / 1000       # in m
        return radius


    def projected_area(self) -> float:
        """ 
        Gives the 2d area of the 3d meteor that faces the direction of velocity,
        or in other words, the area undergoing most air pressure.
 
        """
        return np.pi * self.radius()**2


    def air_friction(self) -> float:
        """
        Calculates the amount of air friction given the projected area and velocity.

        """
        air_friction = -0.65 * self.projected_area(self.radius()) * abs(self.v**2)
        return air_friction


    def total_force(self) -> float:
        """
        Calculates the total force of the meteorite based on its weight and size
        """
        total_force = self.weight() * self.air_friction(self.radius())
        return total_force


    def acceleration(self) -> float:
        """
        Calculates the acceleration of the meteorite based on its size and mass

        >>> x = Comet(15000, 100000, 30)
        >>> x.acceleration(100) < x.acceleration(20)
        True

        >>> type(x.acceleration(10)) == float
        True
        """
        acceleration = self.total_force(self.radius()) / self.m
        return acceleration


    def air_density(self) -> float:
        """
        Calculates the air density using the pyatmos package

        >>> x = Comet(15000, 100000, 30) 
        >>> x.h = 1
        >>> x.air_density() 
        """
        expo_geom = expo(self.h)
        return expo_geom.rho[0]
        # return 40.1

    def change_in_temp(self) -> float:
        radius = self.radius() * 1000
        dT_dt = 1 / radius**2
        return dT_dt


    # Complex Formulas
    def change_in_velocity(self) -> float:
        """
        Calculates the change in velocity over time of the meteorite
        """
        dV_dt: float = -self.C_d * ((self.air_density() * self.projected_area() * \
            self.V_init**2) / self.m) + self.gravity() * np.sin(self.angle)
        print(dV_dt)
        return dV_dt


    def change_in_mass(self) -> float:
        """
        Calculates the change in mass over time of the meteorite
        """
        param1 = (self.C_h * self.air_density() * self.V_init**3) / 2
        param2 = self.sigma * self.T**4

        # print(param1)
        # print(param2)

        value = min(param1, param2)
        # print(value)

        # dM_dt = -self.projected_area() * (value / (self.m * self.Q))
        dM_dt = -self.projected_area() * (value / (self.Q))
        # print(dM_dt)
    #    self.m = self.m + (dM_dt * dt)
        return dM_dt


if __name__ == "__main__":
    import doctest
    doctest.testmod()
