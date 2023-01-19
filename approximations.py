from comet import Comet
import numpy as np


class Approx:

    def __init__(self) -> None:
        return None
        


    def velocity_verlet(self, dt: float, comet: Comet) -> tuple[float]:
        """Verlet approximation per timestep"""
    
        acc = comet.change_in_velocity(2.0)

        """calculate half timestep velocity"""
        v_half_t = comet.v + acc * 1/2 * dt
        
        """calculate movement over timestep"""
        comet.x = comet.x + v_half_t * dt

        """derive new acc for timestep from position"""
        acc2 = comet.change_in_velocity(2.0)

        """calculate velocity for time"""
        comet.v = v_half_t + 1/2 * acc2 * dt
        
        return comet.x, comet.v

    def euler(self, dt: float, comet: Comet, radius: float) -> float:
        dM_dt = comet.change_in_mass(radius)
        comet.m = comet.m + (dM_dt * dt)
        return comet.m

            

        



"""the approximation"""



"""
def euler_approx(maxim: int, step_size: float, t: int, x: int, i:int, start_val: int) -> list[float]:
    arr_steps : list[float] = []
    arr_steps.append(start_val)

    step_num = int(1/step_size)

    for step in [i * step_size for i in range(1, step_num * maxim + 1)]:
        new_val = arr_steps[-1] + (t * step + x * arr_steps[-1] + i) * step_size
        arr_steps.append(new_val)
        
    return arr_steps
"""




    















