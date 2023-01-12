from comet import Comet

"""constants"""
dt = 0.1 # timestep (accuracy)


"""initial conditions"""
x = [0] # initial position
v = [1.8E4] # initial velocity
mass = [10] # intial mass
total_height = 2E5

# time
t = [0]


"""the approximation"""


while x[-1] < total_height: # we should add something for the mass
    
    h = total_height - x[-1]
    acc = Comet.change_in_velocity(h, 2, v[-1], mass[0], 45) # is het v[-1] of v[0] ?????

    """calculate half timestep velocity"""
    v_half_t = v[-1] + acc * 1/2 * dt
    
    """calculate movement over timestep"""
    x.append(x[-1] + v_half_t * dt)

    """derive new acc for timestep from position"""
    h2 = total_height - x[-1]
    acc2 = Comet.change_in_velocity(h2, 2, v[-1], mass[0], 45)

    """calculate velocity for time"""
    v.append(v_half_t + 1/2 * acc2 * dt)

    













# def euler_approx(maxim: int, step_size: float, t: int, x: int, i:int, start_val: int) -> list[float]:
#     arr_steps : list[float] = []
#     arr_steps.append(start_val)

#     step_num = int(1/step_size)

#     for step in [i * step_size for i in range(1, step_num * maxim + 1)]:
#         new_val = arr_steps[-1] + (t * step + x * arr_steps[-1] + i) * step_size
#         arr_steps.append(new_val)
        
#     return arr_steps

