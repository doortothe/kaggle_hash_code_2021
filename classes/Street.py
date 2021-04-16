import pandas as pd

import classes as cl


class Street:

    def __init__(self, name, start_intersection_id, end_intersection_id, length):
        self.id = name
        self.length = int(length)
        self.queue = []  # cars waiting for the light to change
        self.traffic = {i: [] for i in range(self.length)}  # cars currently traveling to the light
        self.start_intersection_id = start_intersection_id
        self.end_intersection_id = end_intersection_id
        self.state = cl.RED

        # statistic variables
        self.street_delay = pd.DataFrame(columns=['tick', 'cars', 'delay'])

    def place_car_in_queue(self, car):
        """
        Place a car at the end of the queue.
        Currently passing Car so i append the id to the list.
        :param car:
        """
        # todo: Should I store the car id or the car itself?
        self.queue.append(car.get_id)

    def place_car_in_traffic(self, car_id):
        """
        Same as place_car_in_queue except traffic array.
        :param car_id:
        """
        self.traffic[self.length - 1].append(car_id)

    @property
    def get_id(self):
        return self.id

    @property
    def get_intersection(self):
        return self.end_intersection_id

    @property
    def get_state(self):
        return self.state

    @property
    def has_queue(self):
        if len(self.queue) > 0:
            return True
        else:
            return False

    @property
    def has_traffic(self):
        """

        :return: the indexes where this street has traffic. If there's no traffic, returns -1
        """
        traffic_values = [k for (k, v) in self.traffic.items() if len(v) > 0]
        # Check if this empty
        if len(traffic_values) == 0:
            return [-1]
        # Add the following if necessary for debug purposes
        # elif len(traffic_values) == 1:
        #     return [traffic_values]
        else:
            return traffic_values

    @property
    def get_queue(self):
        return self.queue

    @property
    def get_traffic(self):
        return self.traffic

    def __repr__(self):
        return str(self.id)

    # todo: implement ability to track delays as feature to reduce in optimization
    def add_delay(self, cars):
        # Count number of cars in queue array and add 1 delay for each
        self.street_delay += len(self.queue)

        # todo: Add delay to the cars stuck in traffic
        pass

    def flip_state(self):
        if self.state == cl.RED:
            self.state = cl.GREEN
        else:
            self.state = cl.RED

    def pop_queue(self):
        """
        Used for a car crossing the street.
        :return: Car that crosses the street. The simulation then uses this car id to call cross_intersection()
        """
        car = self.queue[0]
        self.queue.pop(0)
        return car

    def get_traffic_cars(self, position):
        # todo: add security as mentioned below
        """
        add parameter check if position is less than self.length
        Should I double check if we're actually returning something?
        :param position:
        :return:
        """
        return self.traffic[position]

    def tick_traffic(self):
        # todo: optimize so only move cars in specified traffic areas instead of all
        for i in range(len(self.traffic) - 1):
            self.traffic[i] = self.traffic[i + 1]

        self.traffic[len(self.traffic) - 1] = []
