import numpy as np

class Comet:
    def __init__(self, V_init: float, M_init: float, angle: int, h: float, m: float, v: float, \
            R: int = 6371000, C_d: float = 0.47, C_h: float = 0.1, sigma: float = 5.6697E-8, \
            T: int = 1000, Q: int = 8, g: float = 9.81) -> None:
        
        # constants, nonmutable variables
        self.R = R  # Radius of the Earth  
        self.C_d = C_d # Drag coefficient
        self.C_h = C_h  # Heat transfer coefficient
        self.sigma = sigma    # Stefan-Boltzmann constant       
        self.T = T    # Temperature in K
        self.Q = Q       # Heat of ablation in MJ
        self.g = g    # gravitational constant

        # experimental starting values
        self.angle = angle      # angle of entry
        self.V_init = V_init    # initial velocity
        self.M_init = M_init    # initial mass

        # updating variables
        self.h = h      # distance from the earth (m)
        self.m = m      # mass (kg)
        self.v = v      # velocity (m/s) ??


    
    def comet_assembly(self) -> None:
        """
        Saves the initial values to the updated values for the start of the simulation.

        """
        self.v = self.V_init
        self.m = self.M_init
        self.h = 200000.0  #klopt dit? ja
        

    # Simple Formulas
    def gravity(self) -> float:
        """
        Calculates the gravitation constant at the height of the comet above the earth
        >>> x, y = Comet(15000, 100000, 30, 200000, 90000, 10000), Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.h, y.h = 100, 1000
        >>> x.gravity() > y.gravity()
        True

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.h = 3
        >>> x.gravity() == 9.81 * (1 - 6/x.R)
        True

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
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
        >>> x, y = Comet(15000, 100000, 30, 200000, 90000, 10000), Comet(15000, 10000, 30, 200000, 9000, 10000)
        >>> y.weight() < x.weight()
        True
        
        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> type(x.weight()) == float
        True
        """
        return self.m * self.gravity()


    def projected_area(self, radius: float) -> float:
        """ 
        Gives the 2d area of the 3d meteor that faces the direction of velocity,
        or in other words, the area undergoing most air pressure.
        
        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.projected_area(100.0) > x.projected_area(10.0)
        True

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> type(x.projected_area(100.0)) == float
        True
        """
        return np.pi * radius**2


    def air_friction(self, radius: float) -> float:
        """
        Calculates the amount of air friction given the projected area and velocity.
        
        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.air_friction(100) < x.air_friction(10)
        True

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.air_friction(10) == x.air_friction(10)
        True

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> type(x.air_friction(10)) == float
        True
        """
        air_friction = -0.65 * self.projected_area(radius) * abs(self.v**2)
        return air_friction


    def total_force(self, radius: float) -> float:
        """
        Calculates the total force of the meteorite based on its weight and size

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.total_force(20) < x.total_force(50)
        False

        >>> type(x.total_force(20)) == float
        True

        >>> x.total_force(0) == 0
        True

        """
        total_force = self.weight() * self.air_friction(radius)
        return total_force


    def acceleration(self, radius: float) -> float:
        """
        Calculates the acceleration of the meteorite based on its size and mass

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.acceleration(100) < x.acceleration(20)
        True

        >>> type(x.acceleration(10)) == float
        True
        """
        acceleration = self.total_force(radius) / self.m
        return acceleration


    def air_density(self) -> float:
        """
        Calculates the air density at different heights (h)

        >>> x = Comet(15000, 100000, 30, 200000, 90000, 10000)
        >>> x.air_density()
        5.365972601885816e-07

        >>> x = Comet(15000, 100000, 30, 20000, 90000, 10000) 
        >>> x.air_density()
        0.0015261813207342312

        >>> x = Comet(15000, 100000, 30, 10000, 90000, 10000) 
        >>> x.air_density()
        0.0017562828078283295
        """
        if self.h > 25098.76:
            T = -205.05 + 0.00164 * self.h
            P = 51.97 * ((T + 459.7) / 389.98)**-11.388

        if 11019.13 < self.h < 25098.76:
            T = -70
            P = 473.1 * np.exp(1.73 - 0.000048 * self.h)

        if self.h < 11019.13:
            T = 59 - 0.00356 * self.h
            P = 2116 * (((T + 459.7) / 518.6)) ** 5.256

        air_density: float = P / (1718 * (T + 459.7))
        return air_density 


    # Complex Formulas
    def change_in_velocity(self, radius: float) -> float:
        """
        Calculates the change in velocity over time of the meteorite
        """
        dV_dt: float = -self.C_d * ((self.air_density() * self.projected_area(radius) * \
            self.V_init**2) / self.m) + self.gravity() * np.sin(self.angle)
#        self.v = self.v + dV_dt
        return dV_dt


    def change_in_mass(self, radius: float) -> float:
        """
        Calculates the change in mass over time of the meteorite
        """
        param1 = (self.C_h * self.air_density() * self.V_init**3) / 2 
        param2 = self.sigma * self.T**4

        value = min(param1, param2)

        dM_dt = -self.projected_area(radius) * (value / (self.m * self.Q))
    #    self.m = self.m + dM_dt
        return dM_dt


if __name__ == "__main__":
    import doctest
    doctest.testmod()