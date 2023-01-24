import numpy as np
from pyatmos import expo


class Comet:
    
    def __init__(self, V_init: float, M_init: float, angle: int) -> None:
        
        # constants, nonmutable variables
        self.R: float = 6371000         # Radius of the Earth (m) 
        self.C_d: float = 0.47          # Drag coefficient
        self.C_h: float = 0.045         # Heat transfer coefficient; backed by different source, max val
        self.sigma: float = 5.6697E-8   # Stefan-Boltzmann constant       
        self.T: float = 2073.2          # Temperature (K)   ->  iffy opzoeken
        self.Q: int = 8.26              # Heat of ablation (J)  -> J of MJ???
        self.g: float = 9.81            # gravitational constant (m/s^2)
        self.total_height: float = 2E5  # initial height (m)
        self.density: int = 3.5         # density of ordinary chondrite (kg/m^3)

        # experimental starting values
        self.angle = angle      # angle of entry
        self.V_init = V_init    # initial velocity (m/s)
        self.M_init = M_init    # initial mass (kg)

        # updating variables (with initial values)
        self.h: float = 2E5     # distance from the earth (m)
        self.m = M_init         # mass (kg)
        self.v = V_init         # velocity (m/s) 
        self.x = 0              # distance traveled (m)
        

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


    def air_friction(self) -> float:
        """
        Calculates the amount of air friction given the projected area and velocity.
        
        >>> x = Comet(15000, 100000, 30)
        >>> x.air_friction(100) < x.air_friction(10)
        True
        >>> x = Comet(15000, 100000, 30)
        >>> x.air_friction(10) == x.air_friction(10)
        True
        >>> x = Comet(15000, 100000, 30)
        >>> type(x.air_friction(10)) == float
        True
        """
        air_friction = -0.65 * self.projected_area(self.radius()) * abs(self.v**2)
        return air_friction


    def total_force(self) -> float:
        """
        Calculates the total force of the meteorite based on its weight and size
        >>> x = Comet(15000, 100000, 30)
        >>> x.total_force(20) < x.total_force(50)
        False
        >>> type(x.total_force(20)) == float
        True
        >>> x.total_force(0) == 0
        True
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
        # if self.h > 25098.76:
        #     T = -205.05 + 0.00164 * self.h
        #     P = 51.97 * ((T + 459.7) / 389.98)**-11.388

        # if 11019.13 < self.h < 25098.76:
        #     T = -70
        #     P = 473.1 * np.exp(1.73 - 0.000048 * self.h)

        # if self.h < 11019.13:
        #     T = 59 - 0.00356 * self.h
        #     P = 2116 * (((T + 459.7) / 518.6)) ** 5.256

        # air_density: float = P / (1718 * (T + 459.7))
        # return air_density 
        # return 0.0017562828078283295

        height = self.h / 1000
        expo_geom = expo(height)
        return expo_geom.rho[0]



    # def change_in_velocity(self):
    #     dV_dt = -self.C_d * self.projected_area() * (self.density**(-2/3)) * self.air_density() * (self.m**(-1/3)) * self.v**2
    #     return dV_dt


    # def change_in_mass(self):
    #     dM_dt = -(self.C_h * self.projected_area()) / (2 * self.Q) * (self.density**(-2/3)) * self.air_density() * (self.m**(2/3)) * self.v**3
    #     return dM_dt


    # Complex Formulas
    def change_in_velocity(self) -> float:
        """
        Calculates the change in velocity over time of the meteorite
        """
        # dV_dt: float = -self.C_d * ((self.air_density() * self.projected_area() * \
        #     self.V_init**2) / self.m) + self.gravity() * np.sin(self.angle)

        dV_dt = (-(1/2) * (self.C_d * self.projected_area() * self.air_density() * (self.v**2)) / self.m) + (self.gravity() * np.sin(self.angle))
        return dV_dt


    def change_in_temp(self) -> float:
        radius = self.radius() * 1000
        dT_dt = 1 / radius**2
        self.T += dT_dt * 0.001
        # print(self.T)
        return dT_dt
    

    def change_in_mass(self) -> float:
        """
        Calculates the change in mass over time of the meteorite
        """
        # self.change_in_temp()
        # param1 = (self.C_h * self.air_density() * self.v**3) / 2
        # param2 = self.sigma * self.T**4

        # # # print(param1)
        # # # print(param2)

        # value = min(param1, param2)
        # # # print(value)

        # dM_dt = -self.projected_area() * (value / (self.M_init * self.Q))
        # # # dM_dt = -self.projected_area() * (value / (self.Q))
        # # # print(dM_dt)
        # return dM_dt

        dM_dt = -self.air_density() * self.projected_area() * (self.V_init) / (self.m * self.Q)
        return dM_dt



if __name__ == "__main__":
    import doctest
    doctest.testmod()