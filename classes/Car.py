import pandas as pd


class Car:
    destination: object

    def __init__(self, name, path):
        self.id = name
        self.path = path  # list of street ids
        self.current_street = path[0]
        self.path_index = 0

        # Statistic tracking variables
        self.car_delay = pd.DataFrame(columns=['id', 'street', 'delay'])
        self.end_time = -1

    def __repr__(self):
        return str(self.id)

    def cross_intersection(self):
        self.path_index += 1
        # print("car " + str(self.id) + " crossing from " + self.current_street)
        self.current_street = self.path[self.path_index]

    @property
    def get_current_streetID(self):
        return self.current_street

    @property
    def get_destination(self):
        return self.path[len(self.path) - 1]

    @property
    def get_path(self):
        return self.path

    @property
    def get_id(self):
        return self.id

    @property
    def get_delay(self):
        return self.car_delay

    # todo: implement ability to track delays as feature to reduce in optimization
    def add_delay(self):
        # Check if the street has changed
        if self.current_street != self.car_delay['street']:  # street is different
            # Add new row to delay dataframe/dictionary
            new_row = {'car id': self.id, 'street': self.current_street, 'delay': 1}
            self.car_delay.append(new_row, ignore_index=True)
        else:
            # Add one delay to the latest row
            self.car_delay.at[len(self.car_delay.index) - 1, 'delay'] += 1

    def set_end_time(self, end_time):
        self.end_time = end_time
