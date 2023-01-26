from comet2 import Comet
from approximations import Approx as app
from asteroids import Asteroids
import numpy as np
from numba import jit

filename = 'nasa_dataset\\impacts.csv'
dt = 0.01

asteroids = Asteroids(filename)
V_inits = asteroids.velocity()
M_inits = asteroids.mass()


comet = Comet(V_init=20000, M_init=10, angle=45)

@jit(nopython = True)
def loop(comet: Comet):
    masses = np.zeros(1000000000)
    velocities = np.zeros(1000000000)
    distances = np.zeros(1000000000)
    t: int = 0
    while comet.m > 1E-3 and comet.v > 0 and comet.h > 0:
        
        app.euler(dt, comet)
        app.velocity_verlet(dt, comet)

        masses[t] = comet.m
        velocities[t] = comet.v
        distances[t] = comet.x
        comet.h = comet.h - comet.v * dt * (np.cos(comet.angle * (np.pi / 180)))
        # print(comet.h, '\t\t', comet.m)
        # comet.h -= comet.x
        t += 1
        # print(comet.v)
        return masses, velocities, distances, t

masses, velocities, distances, t = loop(comet)
avg_velos = np.mean(velocities) 
print("Initial velocity:" , velocities[0], "Final velocity:", velocities[-1])
print("Initial mass:", masses[0], "Final mass:", masses[-1])
print("At timestep: ", t)
dist = avg_velos * t
print(dist)

if comet.x >= 1.5E5:
    print("hit")
else:
    print("miss")