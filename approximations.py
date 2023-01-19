from comet import Comet
import numpy as np


class Approx:
    
    def __init__(self) -> None:
        return None
    
    @staticmethod
    def velocity_verlet(dt: float, comet: Comet) -> tuple[float, float]:
        """Verlet approximation per timestep"""
    
        acc = comet.change_in_velocity(comet.r)

        """calculate half timestep velocity"""
        v_half_t = comet.v + acc * 1/2 * dt
        
        """calculate movement over timestep"""
        comet.x = comet.x + v_half_t * dt

        """derive new acc for timestep from position"""
        acc2 = comet.change_in_velocity(comet.r)

        """calculate velocity for time"""
        comet.v = v_half_t + 1/2 * acc2 * dt
        
        return comet.x, comet.v

    @staticmethod
    def euler(dt: float, comet: Comet) -> float:
        dM_dt = comet.change_in_mass(comet.r)
        comet.m = comet.m + (dM_dt * dt)
        return comet.m




    















