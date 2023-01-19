from comet import Comet
from approximations import Approx as app
import numpy as np


dt = 0.0001
comet = Comet(V_init = 2.2E4, M_init=0.9, angle=45)

masses: list[float] = [comet.m]
velocities: list[float] = [comet.v]
distances: list[float] = [0]
t = 0
while comet.x < 2E5 and comet.m > 0:
    mass = app.euler(dt, comet)
    velocity = app.velocity_verlet(dt, comet)

    masses.append(mass)
    velocities.append(comet.v)
    distances.append(comet.x)
    t += dt

print("Final mass: ", masses[-1])
print("At timestep: ", t)

if comet.x >= 2E5:
    print("hit")
else:
    print("miss")