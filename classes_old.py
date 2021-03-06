# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd


def validate_variable(var, var_check):
    """
    Check if variable is within appropriate constraints
    Return the variable if true
    Otherwise, return an error
    :param var: variable being checked
    :param var_check: the variable to check
    :return: var if within proper constraints. Otherwise, raise an error
    """
    # Go through list of variables
    if var_check == 'D' and 1 <= var <= 10 ^ 4:
        return var

    if (var_check == 'I' or var_check == 'S') and 2 <= var <= 100_000:
        return var

    if var_check == 'V' and 2 <= var <= 1_000:
        return var

    if var_check == 'F' and 1 <= var <= 1_000:
        return var

    raise Exception("Inappropriate value for " + var_check + ": " + str(var))


def find(array, idt):
    """

    :param array: list of class has an id field for the id() method
    :param idt: Id we are looking for
    :return: if id is in id(list), return the index. -1 if not
    """
    i = -1
    for x in range(len(array)):
        if array[x].get_id == idt:
            i = x
    return i


RED = 'red'
GREEN = 'green'


# def validate_cars()

class Simulation:
    # todo: create proper documentation
    # todo: remove unused variables/functions
    def __init__(self, duration, num_intersections, num_streets, num_cars, points):
        # Input variables from the file
        self.duration = validate_variable(duration, 'D')
        self.num_intersections = validate_variable(num_intersections, 'I')
        self.num_streets = validate_variable(num_streets, 'S')
        self.num_cars = validate_variable(num_cars, 'S')
        self.points = validate_variable(points, 'F')

        # Simulation variables
        self.score = 0
        self.current_time = 0
        self.streets = []
        self.cars = []
        self.intersections = []

        # Statistic tracking variables
        self.num_cars_score_before_end = 0

        # statistic tracking dataframes
        self.car_delays = pd.DataFrame(columns=['car id', 'street', 'delay'])
        # Just how much data do I want to track here?
        # I'll start simple for now.
        self.score_df = pd.DataFrame(columns=['car id', 'score',
                                              'bonus points', 'time scored',
                                              'delayed'])

        self.street_delay_df = pd.DataFrame(columns=['street'])

    @property
    def get_num_streets(self):
        return self.num_streets

    @property
    def get_num_intersections(self):
        return self.num_intersections

    @property
    def get_num_cars(self):
        return self.num_cars

    @property
    def get_current_time(self):
        return self.current_time

    def set_streets(self, streets):
        # todo: validate parameter is array of streets
        self.streets = streets

    def set_intersections(self, intersections):
        self.intersections = intersections

    def set_cars(self, cars):
        self.cars = cars

        # set the cars into the streets where they belong
        for car in cars:
            # Find the car's current street in the sim's street array
            [street.place_car_in_queue(car) for street in self.streets if street.get_id == car.get_current_streetID]

        # Debug to see if this worked
        # for street in self.streets:
        #     print(street.get_id + ": " + str(street.positions))

    @classmethod
    def read_input(cls, file):
        # Read in the first line, which contains the simulation-wide variables
        f = open(file, 'r')
        line = f.readline().split(' ')

        # Instantiate the Simulation class
        # todo: add documentation on which line part is what
        sim = Simulation(int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]))

        # Create the streets
        streets = []
        intersections = []
        for x in range(sim.get_num_streets):
            line = f.readline().split(' ')
            streets.append(Street(line[2], line[0], line[1], line[3]))

            # Add the new intersection to the list, or add new street to existing intersection
            # Check if current intersection is already in the list
            # todo: rewrite code to look/add new intersections in both line[0] and line[1]
            i = find(intersections, int(line[1]))
            if i > -1:
                # Check if current street is already in the intersection's list
                if line[2] not in intersections[i].get_streets:
                    intersections[i].add_street(line[2])
            else:
                # Add new intersection
                intersections.append(Intersection(line[1], line[2]))

        # Store streets and intersections in the simulation
        # todo: add check to see if num streets found = self.num_streets
        sim.set_streets(streets)

        # todo: add check to see if number of intersections found = self.num_intersections
        sim.set_intersections(intersections)

        # Create the cars
        cars = []
        for y in range(sim.get_num_cars):
            line = f.readline().replace('\n', '').split(
                ' ')  # Need to remove new line character to avoid bug when finding unique streets
            # todo: add security check that line[0] doesn't exceed the number of streets aka line[1:]
            cars.append(Car(y + 1, line[1:]))

        # store cars in the simulation's car array
        sim.set_cars(cars)

        # Close the file
        f.close()
        return sim

    # todo: combine read_input and read_submission so they are called in one line by main.py
    def read_submission(self, file):
        f = open(file, 'r')
        num_schedules = int(f.readline())

        # Read through the file as specified by the first line
        for x in range(num_schedules):
            # This line tell us the intersection we're working with

            intersection = int(f.readline())
            # print("Working on intersection " + intersection)
            # The next line tells us how many lights we're looking at
            num_lights = int(f.readline())

            schedules = []

            # need to be able to reference the streets based on the intersection id
            for y in range(num_lights):
                # Grab the line
                line = f.readline().split(' ')

                # todo: add documentation describing what line parts are what
                # schedule['street'] = line[0]
                # todo: add timer variable constraints (1 <= timer <= duration)
                for i in range(int(line[1])):
                    schedules.append(line[0])

            # Give the schedule to the appropriate intersection
            # todo: add try-except statement in case unable to find intersection for whatever reason
            self.intersections[find(self.intersections, intersection)].set_schedule(pd.Series(schedules))
            # print(intersection)

        #  Finally, cut all unnecessary streets and intersections, where no car will interact with them
        self.streets, self.intersections = self.cut_streets(self.cars, self.streets, self.intersections)

        # for i in self.intersections:
        #     print("id: " + str(i.id))
        #     print('streets: ' + str(i.get_streets))

        # for i in self.intersections:
        #     print(i.get_id)
        #     print(i.get_schedule)
        #     if int(i.get_id) == 2:
        #         print(i.get_schedule.shape[0])

    def create_submission(self, file=None):
        # todo: implement a version for creating a flat submission file for a new input file
        """

        :param file: If none, create new file.
        :return:
        """
        pass

    @classmethod
    def cut_streets(cls, cars, streets, intersections):
        # Create list of all streets and intersections cars touch
        all_streets = pd.DataFrame()

        # todo: optimize
        for i in cars:
            all_street = pd.DataFrame()
            all_street['streets'] = i.get_path

            # grab the intersection ids
            all_street['intersections'] = [streets[find(streets, j)].get_intersection for j in i.get_path]
            all_streets = all_streets.append(all_street)

        # Convert list into pandas series of unique streets
        unique_streets = all_streets['streets'].unique()
        unique_intersections = all_streets['intersections'].unique()

        # Delete all streets not in unique_streets
        # Gather list of streets not in unique_streets
        streets = [street for street in streets if street.get_id in unique_streets]

        # Delete all intersections not in unique_intersections
        # Gather list of intersections not in unique_intersections
        intersections = [it for it in intersections if str(it.get_id) in unique_intersections]

        return streets, intersections

    def run_simulation(self):
        # Remove lights that are always green/red
        self.intersections, self.streets = self.optimize_lights(self.intersections, self.streets)

        # Simulation loop
        for self.current_time in range(self.duration):
            # Record statistics
            # todo: implement in-simulation statistic gathering.
            """
            self.num_cars_score_before_end = length of score_df
            """

            self.tick()
            # self.print_lights(self.current_time, self.intersections, self.streets)
            self.print_cars(self.current_time, self.streets)

        # End of simulation statistic calculating

        # calculate time each scored car spent driving
        self.calculate_statistics()

        # Record dataframes as output
        # todo: find naming schema that can be procedural yet understandable
        with pd.ExcelWriter('data/simulation.xlsx') as writer:
            self.score_df.to_excel(writer, sheet_name='Scores')

    def tick(self):
        # Update traffic light schedules
        for light in self.intersections:
            # Check which light should be on
            self.streets = light.intersection_tick(self.streets)

        # Move cars/count delay
        # todo: implement delay tracking
        for street in self.streets:
            # move cars traveling down the road
            self.move_traffic(street)

            # Move cars in the queue if there is one
            if street.has_queue:
                if street.get_state == GREEN:
                    self.move_queue(street)
                else:
                    self.count_delay(street)

    def move_queue(self, street):
        """
        Helper function
        :param street:
        :return:
        """
        # pop the first member of the queue and have it cross the street
        car = self.cars[find(self.cars, street.pop_queue())]
        car.cross_intersection()

        # Add the car to its new street
        self.streets[find(self.streets, car.get_current_streetID)].place_car_in_traffic(car)

    def count_delay(self, street):
        pass

    def move_traffic(self, street):
        """
        Helper function
        :param street:
        :return:
        """
        traffic_areas = street.has_traffic
        if traffic_areas[0] != -1:
            if traffic_areas[0] == 0:
                # Check if the car(s) reached their final destination
                # todo: move this block of code into a helper function
                for car in street.get_traffic_cars(0):
                    if self.cars[find(self.cars, car)].get_destination == street.get_id:
                        self.score_car(car)
                    else:
                        # Add car to queue
                        street.place_car_in_queue(car)
            # Update the rest of the traffic
            street.tick_traffic()

    def score_car(self, car):
        # calculate score based on car parameters
        if self.current_time <= self.duration:  # If the car was removed before the simulation ended
            bonus_points = self.duration - (self.current_time + 1)
            points = self.points + bonus_points
            self.score += points

            print("Car " + str(car.get_id) + " scores " + str(points) + " points.")

            # Add to the score table
            new_row = {'car id': car.get_id, 'score': points,
                       'bonus points': bonus_points, 'time scored': self.current_time,
                       'delayed': car.get_delay['delay'].sum()}
            self.score_df.append(new_row, ignore_index=True)

        # Otherwise, no score is added

        # todo: record car stats
        """
        Stats to track:
            When car was removed: check
            Points earned: check
            Time spent at red light: check
            Bonus points: check
        """

        # Append car's delay table to the global table
        self.car_delays.append(car.get_delay)

        self.cars.remove(car)

    @classmethod
    def optimize_lights(cls, intersections, streets):
        """
        run_simulation helper function
        :return:
        """
        # Find lights that are always set to on/off and mark as such to optimize later ticks
        remove_list = []
        for i in intersections:
            # A light is always on if only one light is mentioned in a schedule
            if i.get_schedule is None:
                # print("Removing intersection " + str(i.get_id) + " because its always red.")
                remove_list.append(i.get_id)

            # A light is always off if the intersection is not listed in the schedule
            elif i.get_schedule.unique().size == 1:
                # Street to update
                streets[find(streets, i.get_schedule[0])].flip_state()
                # print("Removing intersection " + str(i.get_id) + " because its always green.")

                # Remove light from list of intersections to check each tick
                remove_list.append(i.get_id)
        # Remove intersections scheduled for disposal
        intersections = [r for r in intersections if r.get_id not in remove_list]

        return intersections, streets

    @classmethod
    def print_lights(cls, tick, intersections, streets):
        print("tick: " + str(tick))
        for i in intersections:
            print("\tintersection: " + str(i.get_id))
            for s in i.get_streets:
                print("\t\t" + s + ": " + streets[find(streets, s)].get_state)

    @classmethod
    def print_cars(cls, tick, streets):
        print("tick: " + str(tick))
        for s in streets:
            if s.has_queue or s.has_traffic[0] != -1:
                print('\tstreet: ' + str(s.get_id))

            if s.has_queue:
                print('\t\tQueue: ' + str(s.get_queue))
            if s.has_traffic[0] != -1:
                print('\t\tTraffic: ' + str(s.get_traffic))

    def calculate_statistics(self):
        # todo: implement statistic gathering. Such as:
        """
        amount(%) of cars that arrived before deadline : length of score_df / self.num_cars
        Earliest arrival (points earned, time driven): query earliest score_df
        Latest arrival (and points earned, time driven): query latest score_df
        Average points earned: average points + bonus_points of score_df
        Average time(ticks) driven: time_scored - delay in score_df
        Create graph/database of tracking positions and num lights at a time
        Amount of delay caused by each street per tick
        """
        self.score_df['time driven'] = self.score_df['time scored'] - self.score_df['delayed']

    @classmethod
    def get_street_delays(cls, streets):
        # todo: implement this
        """
        Summarize/append the individual street delay dataframes into a single dataframe
        :param streets:
        :return:
        """
        return None


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
            streets[find(streets, self.schedule.iat[self.cycle_position])].flip_state()
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
            streets[find(streets, previous_position)].flip_state()
            streets[find(streets, current_position)].flip_state()

        return streets

    def __repr__(self):
        return str(self.id)


class Street:

    def __init__(self, name, start_intersection_id, end_intersection_id, length):
        self.id = name
        self.length = int(length)
        self.queue = []  # cars waiting for the light to change
        self.traffic = {i: [] for i in range(self.length)}  # cars currently traveling to the light
        self.start_intersection_id = start_intersection_id
        self.end_intersection_id = end_intersection_id
        self.state = RED

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
        if self.state == RED:
            self.state = GREEN
        else:
            self.state = RED

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
