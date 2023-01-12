import numpy as np

class Comet:

    # Variables 

    # Radius of the Earth
    R = 6371000

    # Drag coefficient
    C_d = 0.47

    # Heat transfer coefficient
    C_h = 0.1

    # Stefan-Boltzmann constant 
    sigma = 5.6697 * 10**-8

    # Temperature in K
    T = 1000

    # Heat of ablation in MJ
    Q = 8


    # Simple Formulas
    def gravity(h):
        g = 9.81

        if h != 0:
            g = g * (1 - (2*h / R))

        return g


    def weight(m, g):
        return m * g


    def projected_area(radius):
        return np.pi * radius**2


    def air_friction(velocity, radius):
        air_friction = -0.65 * projected_area(radius) * abs(velocity**2)
        return air_friction


    def total_force(m, g, velocity, radius):
        total_force = weight(m, g) * air_friction(velocity, radius)
        return total_force


    def acceleration(m, g, velocity, radius):
        acceleration = total_force(m, g, velocity, radius) / m
        return acceleration


    def air_density(h):
        if h > 25098.76:
            T = -205.05 + 0.00164 * h
            P = 51.97 * ((T + 459.7) / 389.98)**-11.388

        if 11019.13 < h < 25098.76:
            T = -70
            P = 473.1 * np.exp(1.73 - 0.000048*h)

        if h < 11019.13:
            T = 59 - 0.00356 * h
            P = 2116 * (((T + 459.7) / 518.6))**5.256

        air_density = P / (1718 * (T + 459.7))
        return air_density 



    # Complex Formulas
    def change_in_velocity(h: float, radius: float, init_V: int, m: float, angle: int):
        dV_dt = -C_d * ((air_density(h) * projected_area(radius) * init_V**2) / m) + gravity(h) * np.sin(angle)
        return dV_dt


    def change_in_mass(radius, h, init_V, m):
        param1 = (C_h * air_density(h) * init_V**3) / 2 
        param2 = sigma * T**4

        value = min(param1, param2)

        dM_dt = -projected_area(radius) *  (value / (m * Q))
        return dM_dt
