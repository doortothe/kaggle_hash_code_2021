import pandas as pd

import classes as cl


class Intersection:

    def __init__(self, name, street):
        self.id = int(name)
        self.streets = [street]  # List of street ids of streets that meet at this intersection

        # Schedule variables
        self.always_on = False
        self.always_off = False
        self.cycle_position = -1
        self.schedule = None

        # Statistic variables
        """
        Gonna operate under the assumption that a given intersection can't have more than
        4 streets go through it at a time 
        """
        # todo: (security) check to see max number of streets an intersection has in the submission file
        # then implement dynamic way to add columns ala dynamic length of Street traffic dictionary
        # self.intersection_df_columns = []
        self.intersection_delay_df = pd.DataFrame(columns=['tick', 'total delay',
                                                           'street 1', 's1 delay',
                                                           'street 2', 's2 delay',
                                                           'street 3', 's3 delay',
                                                           'street 4', 's4 delay'])

    def set_schedule(self, schedule):
        self.schedule = schedule

        # print(self.schedule)

    def add_street(self, street_id):
        self.streets.append(street_id)

    def add_delay(self, streets, tick):
        """
        Call this function after calculating delay for the streets first
        :param tick: Current tick
        :param streets: list of streets from Simulation for Intersection to query
        """
        new_row = {'tick': tick}
        # todo: (optimize) find more dynamic way to calculate total_delay
        total_delay = 0

        for i in range(4):
            new_row['street ' + str(i + 1)] = self.streets[i]
            current_column = 's' + str(i + 1) + ' delay'
            new_row[current_column] = streets[cl.find(streets, self.streets[i])].get_current_delay()
            total_delay += new_row[current_column]

        # Get total delay
        new_row['total delay'] = total_delay

        # Add new row to the dataframe
        self.intersection_delay_df.append(new_row, ignore_index=True)

    def set_always_on(self):
        # todo: add check/security so that always_on/always_off can't both be on
        """
        Should only be called in the first tick of a simulation
        :return:
        """

        self.always_on = True

    def set_always_off(self):
        # todo: add check/security so that always_on/always_off can't both be on
        """
        Should only be called in the first tick of a simulation
        :return:
        """
        self.always_off = True
        # light is off by default, so no need to change it

    def intersection_tick(self, streets):
        # todo (cleanup): make function similar to functional programming
        # if this is the first tick
        if self.cycle_position == -1:
            self.cycle_position += 1
            streets[cl.find(streets, self.schedule.iat[self.cycle_position])].flip_state()
            return streets

        previous_position = self.schedule.iat[self.cycle_position]
        # increment current cycle position
        if self.cycle_position + 1 == len(self.schedule):
            # Reset the timer to 1 if it reached the end
            self.cycle_position = 0
        else:
            self.cycle_position += 1
        # print(self.cycle_position)
        current_position = self.schedule.iat[self.cycle_position]

        # Check if lights need to change
        if previous_position != current_position:
            # Turn off previous position and turn on current position
            streets[cl.find(streets, previous_position)].flip_state()
            streets[cl.find(streets, current_position)].flip_state()

        return streets

    def __repr__(self):
        return str(self.id)

    @property
    def get_id(self):
        return self.id

    @property
    def get_streets(self):
        return self.streets

    @property
    def get_schedule_position(self):
        return self.cycle_position

    @property
    def get_schedule(self):
        return self.schedule

    @property
    def get_delay_df(self):
        return self.intersection_delay_df
