from comet2 import Comet
from approximations import Approx as app
from asteroids import Asteroids
import numpy as np
from numba import jit
import matplotlib.pyplot as plt

filename = 'nasa_dataset\\impacts.csv'
dt = 0.01

asteroids = Asteroids(filename)
V_inits = asteroids.velocity()
M_inits = asteroids.mass()

init_velo = [10000, 14000, 18000, 22000, 26000, 30000, 34000, 38000]
init_mass = [0.05, 0.1, 0.2, 0.72, 2.64, 13.5, 132, 13000]



@jit(forceobj = True)
def loop(V_init, M_init, angle=45):

    comet = Comet(V_init=V_init, M_init=M_init, angle=45)

    masses = np.zeros(900000)
    velocities = np.zeros(900000)
    distances = np.zeros(900000)
    t: int = 0
    while comet.m > 0 and comet.v > 0 and comet.h > 0 and t/dt < 900000:
        
        app.euler(dt, comet)
        app.velocity_verlet(dt, comet)

        masses[int(t/dt)] = comet.m
        velocities[int(t/dt)] = comet.v
        distances[int(t/dt)] = comet.x
        comet.h = comet.h - comet.v * dt * (np.cos(comet.angle * (np.pi / 180)))
        # print(comet.h, '\t\t', comet.m)
        t += dt
        # print(comet.v)
    return masses, velocities, distances, t

errors: list[float] = []

for i in range(len(init_velo)):
    masses, velocities, distances, t = loop(init_velo[i], init_mass[i])


    avg_velos = np.mean(velocities) 
    # print("Initial velocity:" , velocities[0], "Final velocity:", velocities[int(t/dt) - 1])
    # print("Initial mass:", masses[0], "Final mass:", masses[int(t/dt) - 1])
    # print("At timestep: ", t * dt)
    if masses[int(t/dt) - 1] < 0:
        erro = 0.02 / masses[0]
    else: erro = (0.02 - masses[int(t/dt) - 1]) / masses[0]
    errors.append(erro)



    # dist = avg_velos * t
    # print(dist)

    # if comet.h <= 0:
    #     print("hit")
    # else:
    #     print("miss")
plt.plot(errors)
plt.show()