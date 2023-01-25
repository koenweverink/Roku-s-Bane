from comet2 import Comet
from approximations import Approx as app
from asteroids import Asteroids
import numpy as np

filename = 'nasa_dataset\\impacts.csv'
dt = 0.001

asteroids = Asteroids(filename)
V_inits = asteroids.velocity()
M_inits = asteroids.mass()


comet = Comet(V_init = 20000, M_init=0.001, angle=45)

masses: list[float] = [comet.m]
velocities: list[float] = [comet.v]
distances: list[float] = [0]

t = 0
while comet.x < 2E5 and comet.m > 0 and comet.v > 0 and comet.h > 0:
    mass = app.euler(dt, comet)
    velocity = app.velocity_verlet(dt, comet)

    masses.append(mass)
    velocities.append(comet.v)
    distances.append(comet.x)
    comet.h = comet.h - comet.v * dt * (np.cos(comet.angle * (np.pi / 180)))
    print(comet.h)
    # comet.h -= comet.x
    t += dt
    # print(comet.v)

print("Initial velocity:" , velocities[0], "Final velocity:", velocities[-1])
print("Initial mass:", masses[0], "Final mass:", masses[-1])
print("At timestep: ", t)
# print(masses)

if comet.x >= 2E5:
    print("hit")
else:
    print("miss")