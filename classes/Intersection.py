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
        # todo: implement intersection delay tracking
        self.delay = 0

    def set_schedule(self, schedule):
        self.schedule = schedule

        # print(self.schedule)

    def add_street(self, street_id):
        self.streets.append(street_id)

    def add_delay(self):
        self.delay += 1

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
