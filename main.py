import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.animation import FuncAnimation

class Simulator():
    def __init__(self):
        self.passengers_booked_seats = list(range(96))
        self.available_seats = list(range(96))
        random.shuffle(self.passengers_booked_seats)
        self.is_at_his_place = False
        self.at_good_places = []

        self.seat_status = np.full((16, 7), -1)

    def is_available(self, seat):
        return seat in self.available_seats
    
    def seat(self, passenger):
        if self.is_available(self.passengers_booked_seats[passenger]):
            place = self.passengers_booked_seats[passenger]
            self.is_at_his_place = True
        else:
            place = random.choice(self.available_seats)
            self.is_at_his_place = False

        self.available_seats.remove(place)
        self.at_good_places.append(self.is_at_his_place)
        
        # Visual Part
        row = place // 6
        col = place % 6
        if col >= 3:
            col += 1
        self.seat_status[row, col] = 1 if self.is_at_his_place else 0

    def firstPassengerSeat(self):
        place = random.choice(self.available_seats)
        self.available_seats.remove(place)
        self.is_at_his_place = False
        self.at_good_places.append(self.is_at_his_place)
        
        # Visual Part
        row = place // 6
        col = place % 6
        if col >= 3:
            col += 1
        self.seat_status[row, col] = 0

    def run_step(self, passenger):
        if passenger == 0:
            self.firstPassengerSeat()
        else:
            self.seat(passenger)
        return self.seat_status

def visualize():
    simu = Simulator()

    
    fig, ax = plt.subplots(figsize=(8, 12))
    cmap = colors.ListedColormap(['gray', 'red', 'green'])
    bounds = [-1, 0, 1, 2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    def update(frame):
        seat_status = simu.run_step(frame)
        ax.clear()
        ax.imshow(seat_status, cmap=cmap, norm=norm)
        ax.set_title(f"Passenger {frame + 1} boarding")
        ax.axis("off")

    ani = FuncAnimation(fig, update, frames=range(96), repeat=False)
    plt.show()

visualize()
