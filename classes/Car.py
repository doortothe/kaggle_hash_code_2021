import pandas as pd


class Car:
    # todo (documentation): Add/complete documentation text here
    destination: object

    def __init__(self, name, path):
        self.id = name
        self.path = path  # list of street ids
        self.current_street = path[0]
        self.path_index = 0

        # Statistic tracking variables
        self.car_delay_df = pd.DataFrame(columns=['id', 'street', 'delay', 'tick'])
        self.end_time = -1

    def cross_intersection(self):
        self.path_index += 1
        # print("car " + str(self.id) + " crossing from " + self.current_street)
        self.current_street = self.path[self.path_index]

    def add_delay(self, tick):
        # Check if the street has changed
        if self.current_street != self.car_delay_df['street']:  # street is different
            # Add new row to delay dataframe/dictionary
            new_row = {'car id': self.id, 'street': self.current_street, 'delay': 1, 'tick': tick}
            self.car_delay_df.append(new_row, ignore_index=True)
        else:
            # Add one delay to the latest row
            self.car_delay_df.at[len(self.car_delay_df.index) - 1, 'delay'] += 1

    # todo (code cleanup): check if need to delete this method
    def set_end_time(self, end_time):
        self.end_time = end_time

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
    def get_delay_df(self):
        return self.car_delay_df

    def __repr__(self):
        return str(self.id)
