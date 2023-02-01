import pandas as pd
import numpy as np


class Asteroids:
    def __init__(self, filename) -> None:
        self.filename = filename

        # Read CSV
        self.df = pd.read_csv(self.filename)

        # Drop Columns not interesting for mow
        columns_to_drop = ['Maximum Palermo Scale', 'Cumulative Palermo Scale', 'Asteroid Magnitude', 'Maximum Torino Scale']
        self.df.drop(columns_to_drop, axis=1, inplace=True)

        # Sort descending by Cumulative Impact Probability
        self.df.sort_values('Cumulative Impact Probability', ascending=False)


    def velocity(self):
        """
        Gets the velocity of each asteroid from NASA's impacts.csv 
        and transforms it from km/s to m/s.
        """
        velocity_list_kms = self.df['Asteroid Velocity'].to_list()
        velocity_list_ms = [velocity * 1000 for velocity in velocity_list_kms]

        return velocity_list_ms
    

    def mass(self):
        """
        Gets the diameter (km) of each asteroid from NASA's impacts.csv and transforms 
        it to mass in kg, by using the density of an ordinary chondrite (3500 kg/m^3)
        """
        diameter_list = self.df['Asteroid Diameter (km)'].to_list()

        # in meter 
        radius_list = [(diameter / 2 * 1000) for diameter in diameter_list]

        # in m^3
        volume_list = [((4/3) * np.pi * (radius**3)) for radius in radius_list]

        # in kg
        mass_list = [volume * 3500 for volume in volume_list]

        return mass_list