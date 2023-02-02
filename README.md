# Roku-s-Bane
Project Computational Science

University of Amsterdam

Eva Peet (12702803), Nathan Pieterse (12649724) and Koen Weverink (14711982)


## Project description
This project simulates asteroids entering Earth's atmospere using both Euler and Velocity Verlet to solve differential equations.

### comet.py
This script contains a class to store the different variables of an asteroid, such as its initial velocity, initial mass and angle of entry. The differential equations, as well as the air density equation are also included.

### approximations.py
This script contains the code that performs the Euler and the Velocity Verlet approximation.

### asteroids.py
This script contains the code that handles NASA's impacts.csv. It gets the velocity in m/s and transforms the diameter to mass.

### analysis.ipynb
This notebook is the core of the project. It runs the simulation, validates it and analyses it by plotting:
- The relation between normalized final mass, initial velocity and angle
- The impact of initial velocity on the rate of ablation
- The impact of the angle on the rate of ablation
- A sensitivity analysis of initial velocity and angle

## Running guide
In order to run the model, perform the following steps:

1. Install the required packages by navigating to the Roku-s-Bane directory and typing in a terminal: pip install -r requirements.txt
2. Open analysis.ipynb in a preferred notebook editor
3. Run the preferred cells, or simply press 'run all' (The 'run all' will take approximately 3-5 minutes)
4. A .png will appear in the same folder, named: reproduced_fig.png. The figure to which this newly generated png needs to be compared to is already present in the folder, named: fig_to_reproduce.png
