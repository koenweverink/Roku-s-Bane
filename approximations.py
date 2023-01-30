from comet2 import Comet
import numpy as np


class Approx:
    
    def __init__(self) -> None:
        return None
    
    @staticmethod
    def velocity_verlet(dt: float, comet: Comet) -> None:
        """
        Verlet approximation of acceleration.
        """
    
        acc = comet.change_in_velocity()

        # calculate half timestep velocity
        v_half_t = comet.v + acc * 1/2 * dt
        
        # calculate movement over timestep
        comet.w += v_half_t * dt * (np.sin(comet.angle * (np.pi / 180)))
        comet.h -= v_half_t * dt * (np.cos(comet.angle * (np.pi / 180)))

        # derive new acc for timestep from position
        acc = comet.change_in_velocity()

        # calculate velocity for end timestep
        comet.v = v_half_t + 1/2 * acc * dt
        
        return None

    @staticmethod
    def euler(dt: float, comet: Comet) -> None:
        """
        Euler approximation of change in mass.
        """
        dM_dt = comet.change_in_mass()

        comet.m += dM_dt * dt
        return None




    















