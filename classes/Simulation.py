import pandas as pd

import classes as cl

from . import Car, Intersection, Street

from datetime import datetime


class Simulation:
    # todo (documentation): create proper documentation
    # todo (code cleaning): remove unused variables/functions
    def __init__(self, duration, num_intersections, num_streets, num_cars, points):
        # Input variables from the file
        self.duration = cl.validate_variable(duration, 'D')
        self.num_intersections = cl.validate_variable(num_intersections, 'I')
        self.num_streets = cl.validate_variable(num_streets, 'S')
        self.num_cars = cl.validate_variable(num_cars, 'S')
        self.points = cl.validate_variable(points, 'F')

        # Simulation variables
        self.score = 0
        self.current_time = 0
        self.streets = []
        self.cars = []
        self.intersections = []

        # Statistic tracking variables
        self.num_cars_score_before_end = 0

        # statistic tracking dataframes
        self.car_delays_df = pd.DataFrame(columns=['car id', 'street', 'delay'])
        # Just how much data do I want to track here?
        # I'll start simple for now.
        self.score_df = pd.DataFrame(columns=['car id', 'score',
                                              'bonus points', 'time scored',
                                              'delayed'])
        # todo (task): Flesh out these dataframes
        self.street_delays_df = None
        self.intersection_delays_df = pd.DataFrame()
        self.general_stats_df = pd.DataFrame()

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
            streets.append(Street.Street(line[2], line[0], line[1], line[3]))

            # Add the new intersection to the list, or add new street to existing intersection
            # Check if current intersection is already in the list
            # todo: rewrite code to look/add new intersections in both line[0] and line[1]
            i = cl.find(intersections, int(line[1]))
            if i > -1:
                # Check if current street is already in the intersection's list
                if line[2] not in intersections[i].get_streets:
                    intersections[i].add_street(line[2])
            else:
                # Add new intersection
                intersections.append(Intersection.Intersection(line[1], line[2]))

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
            cars.append(Car.Car(y + 1, line[1:]))

        # store cars in the simulation's car array
        sim.set_cars(cars)

        # Close the file
        f.close()
        return sim

    # todo (user-friendliness): combine read_input and read_submission so they are called in one line by main.py
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
            self.intersections[cl.find(self.intersections, intersection)].set_schedule(pd.Series(schedules))
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

        # todo (optimization): optimize
        for i in cars:
            all_street = pd.DataFrame()
            all_street['streets'] = i.get_path

            # grab the intersection ids
            all_street['intersections'] = [streets[cl.find(streets, j)].get_intersection for j in i.get_path]
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
            # todo (task): implement in-simulation statistic gathering.
            """

            """

            self.tick()
            # self.print_lights(self.current_time, self.intersections, self.streets)
            # self.print_cars(self.current_time, self.streets)

        # End of simulation statistic calculating

        # Append car_dfs for cars that did not reach their destination
        self.score_df, self.car_delays_df = self.car_cleanup(self.cars, self.score_df, self.car_delays_df)

        # Append individual street and intersection dataframes into one combined dataframe
        self.append_dfs()

        # calculate time each scored car spent driving
        self.calculate_statistics()

        # Record dataframes as output
        self.publish_statistics()

    def tick(self):
        # Update traffic light schedules
        for light in self.intersections:
            # Check which light should be on
            self.streets = light.intersection_tick(self.streets)

        # Move cars/count delay
        for street in self.streets:
            # move cars traveling down the road
            self.move_traffic(street)

            # Move cars in the queue if there is one
            if street.has_queue:
                if street.get_state == cl.GREEN:
                    self.move_queue(street)
                else:
                    # Calling this method will also add delay to the cars
                    street.add_delay(self.cars)

    def move_queue(self, street):
        """
        Helper function
        :param street:
        :return:
        """
        # pop the first member of the queue and have it cross the street
        car = self.cars[cl.find(self.cars, street.pop_queue())]
        car.cross_intersection()

        # Add the car to its new street
        self.streets[cl.find(self.streets, car.get_current_streetID)].place_car_in_traffic(car)

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
                # todo (clean code): move this block of code into a helper function
                for car in street.get_traffic_cars(0):
                    if self.cars[cl.find(self.cars, car)].get_destination == street.get_id:
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

            """
            Car stats tracked:
                When car was removed
                Points earned
                Time spent at red light
                Bonus points
            """
            # Add to the score table
            new_row = {
                'car id': car.get_id,
                'score': points,
                'bonus points': bonus_points,
                'time scored': self.current_time,
                'delayed': car.get_delay_df['delay'].sum(skipna=True)
            }
            self.score_df.append(new_row, ignore_index=True)

        # Otherwise, no score is added

        # Append car's delay table to the global car delay table
        self.car_delays_df.append(car.get_delay_df, ignore_index=True)

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
                streets[cl.find(streets, i.get_schedule[0])].flip_state()
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
                print("\t\t" + s + ": " + streets[cl.find(streets, s)].get_state)

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
        # todo (task): implement statistic gathering. Such as:
        """
        Create graph/database of tracking positions and num lights at a time
        Amount of delay caused by each street per tick
        """
        self.score_df['time driven'] = self.score_df['time scored'] - self.score_df['delayed']

        # Create general statistics dataframe
        self.create_general_df()

    @classmethod
    def car_cleanup(cls, cars, score_df, car_delays_df):
        # todo (task): implement this
        """
        Record stats for all cars that didn't reach their destination
        :return:
        """
        # todo (optimize): find way to reuse score car method for this purpose
        for car in cars:
            new_row = {
                'car id': car.get_id,
                'score': None,
                'bonus points': None,
                # todo (during machine learning analysis): should I set the time for null or end of the simulation?
                'time scored': None,
                'delayed': car.get_delay_df['delay'].sum(skipna=True)
            }

            # Append to the score dataframe
            score_df.append(new_row, ignore_index=True)

            # Append car's delay table to teh global car delay table
            car_delays_df.append(car.get_delay_df, ignore_index=True)

        return score_df, car_delays_df

    def append_dfs(self):
        """
        This function compiles the individual street and intersection delay dataframes into global dataframes
        :return:
        """
        self.street_delays_df = self.append_street_delays(self.streets)
        self.intersection_delays_df = self.append_intersection_delays(self.intersections)

    def create_general_df(self):
        # todo (As machine learning progresses): Add more statistics to gather.
        # Gathers the following statistics into a table
        """
        amount(%) of cars that arrived before deadline : length of score_df / self.num_cars
        Earliest arrival (points earned, time driven): query earliest score_df
        Latest arrival (and points earned, time driven): query latest score_df
        Average points earned: average points + bonus_points of score_df
        Average time(ticks) driven:
        :return:
        """
        general_stats = {
            #todo(same as above): finish the string saying which car was earliest, when, and points earned
            'Earliest Arrival': "",

            #todo(same as above): finish string saying which car was latest, when, and points earned
            'Latest Arrival': "",

            'Num cars completed': len(self.score_df.index),
            '% cars completed': round((len(self.score_df.index) / self.num_cars) * 100, 2),

            # todo (same as above): calculate standard deviations
            'Average points earned': round(self.score_df['score'].mean(skipna=True), 2),
            'Average bonus points earned': round(self.score_df['bonus points'].mean(skipna=True), 2),
            'Average time driving': round(self.score_df['time driven'].mean(skipna=True), 2)
        }

        """
        During analysis of machine learning progress, I want to compile the multiple general_dataframes as a
        bird's eye view of the progress made in each iteration.
        
        Do distribution analysis of points/bonus points data
        """

        return pd.DataFrame(general_stats)

    def publish_statistics(self):
        # todo (task): find naming schema that can be procedural yet understandable
        # for now, using the datetime
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with pd.ExcelWriter('data/simulation' + dt_string + '.xlsx') as writer:
            self.general_stats_df.to_excel(writer, sheet_name='General')
            self.score_df.to_excel(writer, sheet_name='Scores')
            self.street_delays_df.to_excel(writer, sheet_name='Streets')
            self.car_delays_df.to_excel(writer, sheet_name='Cars')
            self.intersection_delays_df.to_excel(writer, sheet_name='Intersections')

    def formulate_initial_submission(self):
        # todo (task: after delay tracking and before machine learning implementation): implement this function
        """
        Split the function into 4 main steps:
            Check the max number of streets an intersection can have.
            Find streets that cars won't travel and cut them from consideration
            Find intersections that should always be on/off
            Create basic submission file where every traffic light has a one second rotation
        :return:
        """

    @classmethod
    def append_street_delays(cls, streets):
        """
        Summarize/append the individual street delay dataframes into a single dataframe
        :param streets:
        :return:
        """
        # todo (optimize): check if I can do this in one line with list comprehension
        temp_df = pd.DataFrame()
        for i in streets:
            temp_df.append(i.get_delay_df(), ignore_index=True)

        return temp_df

    @classmethod
    def append_intersection_delays(cls, intersections):
        # todo (optimize): check if I can do this in one line with list comprehension
        temp_df = pd.DataFrame()

        for i in intersections:
            temp_df.append(i.get_delay_df(), ignore_index=True)

        return temp_df


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
