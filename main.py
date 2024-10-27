import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.animation import FuncAnimation
import argparse
import imageio

class Simulator:
    def __init__(self, mode='visualization'):
        self.passengers_booked_seats = list(range(100))
        random.shuffle(self.passengers_booked_seats)
        self.available_seats = list(range(100))
        self.is_at_his_place = False
        self.at_good_places = []
        self.mode = mode

        self.seat_status = np.full((10, 11), -1)
        for i in range(10):
            self.seat_status[i][5]=2

    def reset(self):
        self.passengers_booked_seats = list(range(100))
        self.available_seats = list(range(100))
        random.shuffle(self.passengers_booked_seats)
        self.is_at_his_place = False
        self.at_good_places = []
        self.seat_status = np.full((10, 11), -1)
        for i in range(10):
            self.seat_status[i][5]=2

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
        row = place // 10
        col = place % 10
        if col >= 5:  # Shift column for the aisle
            col += 1
        self.seat_status[row, col] = 1 if self.is_at_his_place else 0

    def firstPassengerSeat(self):
        place = random.choice(self.available_seats)
        self.available_seats.remove(place)
        self.is_at_his_place = False
        self.at_good_places.append(self.is_at_his_place)
        
        # Visual Part
        row = place // 10
        col = place % 10
        if col >= 5:  # Shift column for the aisle
            col += 1
        self.seat_status[row, col] = 0

    def run_step(self, passenger):
        if passenger == 0:
            self.firstPassengerSeat()
        else:
            self.seat(passenger)
        return self.seat_status

def visualize():
    simu = Simulator(mode='visualization')  # Mode visualisation
    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = colors.ListedColormap(['lightgrey', 'salmon', 'lightgreen', 'blue'])
    bounds = [-1, 0, 1, 2, 3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    simu.firstPassengerSeat()

    frames = []

    def update(frame):
        if frame > 0:
            simu.seat(frame)
        seat_status = simu.seat_status
        ax.clear()
        ax.imshow(seat_status, cmap=cmap, norm=norm)
        ax.set_title(f"Passenger {frame + 1} boarding")
        ax.axis("off")

        plt.savefig(f'results/frame_{frame}.png')
        frames.append(imageio.imread(f'results/frame_{frame}.png'))

    ani = FuncAnimation(fig, update, frames=range(100), repeat=False)
    plt.show()
    imageio.mimsave('airplane_simulation.gif', frames, fps=30)

def display_probability(trials):
    simu = Simulator()
    success_count = 0
    not_at_place_count = 0
    success_list = []
    not_at_place_list = []

    for _ in range(trials):
        simu.reset()
        simu.firstPassengerSeat()
        for passenger in range(1, 100):
            simu.seat(passenger)
        
        last_passenger_success = simu.at_good_places[-1]
        success_list.append(last_passenger_success)
        
        if last_passenger_success:
            success_count += 1
        
        not_at_place = sum(1 for status in simu.at_good_places if not status)
        not_at_place_list.append(not_at_place)
        not_at_place_count += not_at_place

    probability = success_count / trials
    average_not_at_place = not_at_place_count / trials
    print(f"Probability that the last passenger got their assigned seat: {probability:.2f} based on {trials} trials.")
    print(f"Average number of passengers not at their places: {average_not_at_place:.2f}")

    plt.figure(figsize=(12, 6))

    # Distribution of True/False for last passenger
    labels = ['Last Passenger at Place', 'Last Passenger Not at Place']
    sizes = [success_count, trials - success_count]
    plt.subplot(1, 2, 1)
    plt.bar(labels, sizes, color=['green', 'red'])
    plt.title('Distribution of Last Passenger Results')
    plt.ylabel('Number of Trials')

    # Add probability text on the bar graph
    plt.text(0, success_count + 5, f'Probability: {probability:.2f}', ha='center', fontsize=12, color='black')
    
    # Average number of passengers not at their place
    plt.subplot(1, 2, 2)
    plt.hist(not_at_place_list, bins=range(0, 100), alpha=0.7, color='blue', edgecolor='black')
    plt.title('Distribution of Passengers Not at Their Places')
    plt.xlabel('Number of Passengers Not at Their Places')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose the mode of operation.')
    parser.add_argument('mode', choices=['visualization', 'probability'],
                        help='Mode of operation: "visualization" or "probability"')
    parser.add_argument('--nb_trials', default = 10000, required=False, help='For mode operation, number of simulations used to calculate the probability')
    args = parser.parse_args()
    
    if args.mode == 'visualization':
        visualize()
    elif args.mode == 'probability':
        display_probability(int(args.nb_trials))