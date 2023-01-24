from comet2 import Comet
from approximations import Approx as app
import numpy as np


dt = 0.001
comet = Comet(V_init = 2.2E4, M_init=1.5, angle=45)

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
    # comet.h -= comet.x
    t += dt
    # print(comet.v)

print("Initial velocity:" , velocities[0], "Final velocity:", velocities[-1])
print("Initial mass:", masses[0], "Final mass:", masses[-1])
print("At timestep: ", t)
# print(velocities)

if comet.x >= 2E5:
    print("hit")
else:
    print("miss")