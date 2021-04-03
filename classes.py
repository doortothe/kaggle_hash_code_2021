# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


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


# def validate_cars()

class Simulation:
    def __init__(self, duration, num_intersections, num_streets, num_cars, points):
        # Input variables from the file
        self.duration = validate_variable(duration, 'D')
        self.num_intersections = validate_variable(num_intersections, 'I')
        self.num_streets = validate_variable(num_streets, 'S')
        self.num_cars = validate_variable(num_cars, 'S')
        self.points = validate_variable(points, 'F')

        self.score = 0
        self.current_time = 0
        self.streets = []
        self.cars = []
        self.intersections = []

    @property
    def get_num_streets(self):
        return self.num_streets

    @property
    def get_num_intersections(self):
        return self.num_intersections

    @property
    def get_num_cars(self):
        return self.num_cars

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
            [street.place_car(car) for street in self.streets if street.get_id == car.get_current_streetID]

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
        for x in range(0, sim.get_num_streets):
            line = f.readline().split(' ')
            streets.append(Street(line[2], line[0], line[1], line[3]))

            # Add the new intersection to the list, or add new street to existing intersection
            # Check if current intersection is already in the list
            i = find(intersections, line[1])
            if i > -1:
                # Check if current street is already in the intersection's list
                if line[2] not in intersections[i].get_streets:
                    intersections[i].add_street(line[2])
            else:
                # Add new intersection
                intersections.append(Intersection(line[1], line[2]))

        # Store streets and intersections in the simulation
        sim.set_streets(streets)
        sim.set_intersections(intersections)

        # Create the cars
        cars = []
        for y in range(0, sim.get_num_cars):
            line = f.readline().split(' ')
            cars.append(Car(line[0], line[1:]))

        # store cars in the simulation's car array
        sim.set_cars(cars)

        # Close the file
        f.close()
        return sim

    def read_submission(self, file):
        f = open(file, 'r')
        num_schedules = int(f.readline())

        # Read through the file as specified by the first line
        for x in range(num_schedules):
            # This line tell us the intersection we're working with
            intersection = f.readline()

            # The next line tells us how many lights we're looking at
            num_lights = int(f.readline())

            # need to be able to reference the streets based on the intersection id

            for y in range(num_lights):
                # Grab the line
                line = f.readline().split(' ')

    def create_submission(self):
        pass

    def score(self, car):
        # calculate score based on car parameters
        if self.current_time <= self.duration:  # If the car was removed before the simulation ended
            self.score += self.points + (self.duration - self.current_time)
        # Otherwise, no score is added

        # Remove car from the simulation
        pass

    def tick(self):
        # Check traffic light schedules

        # Move cars

        # Check if car reached its destination
        pass

    # todo: find and cut unused streets to reduce number of features in optimization
    def cut_streets(self):
        pass

    # todo: implement optimization method

    # todo: implement method to find statistics. Such as:
    """
    amount(%) of cars that arrived before deadline.
    Earlist arrival (points earned, time driven)
    Latest arrival (and points earned, time driven)
    Average points earned
    Average time(ticks) driven
    Create graph/database of tracking positions and num lights at a time
    Create visualizations of such
    """


class Car:
    destination: object

    def __init__(self, name, path):
        self.id = name
        self.path = path  # list of street ids
        self.current_street = path[0]
        self.path_index = 0
        self.destination = path[len(path) - 1]
        # self.position = None
        self.car_delay = 0

    def __repr__(self):
        return self.id

    def cross_intersection(self):
        self.path_index += 1
        self.current_street = self.path[self.path_index]

    @property
    def get_current_streetID(self):
        return self.current_street

    @property
    def get_destination(self):
        return self.destination

    @property
    def get_id(self):
        return self.id

        # def set_position(self, pos):
        # self.position = pos

    # todo: implement ability to track delays as feature to reduce in optimization


class TrafficLight:
    RED = 0
    GREEN = 1

    def __init__(self, street):
        self.state = self.RED
        self.street_id = street


class Intersection:

    def __init__(self, name, street):
        self.id = name
        self.streets = [street]  # List of street ids of streets that meet at this intersection
        self.schedule = 0
        # self.cycle_length
        self.cycle_position = 0
        self.delay = 0

    def set_schedule(self, schedule):
        self.schedule = schedule

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

    def __repr__(self):
        return self.id


class Street:

    def __init__(self, name, start_intersection_id, end_intersection_id, length):
        self.id = name
        self.length = int(length)
        self.positions = [None] * self.length  # Initialize as empty street
        self.start_intersection_id = start_intersection_id
        self.end_intersection_id = end_intersection_id
        self.light = TrafficLight(self.id)
        self.street_delay = 0

    def place_car(self, car):
        """
        Place a car at the latest available space in the street.
        Assumes there is open space
        """
        # Find first null value in the list
        self.positions[self.positions.index(None)] = car

    @property
    def has_space(self):
        if None in self.positions:
            return True

        return False

    @property
    def get_id(self):
        return self.id

    def __repr__(self):
        return self.id

    # todo: implement ability to track delays as feature to reduce in optimization
    def add_delay(self):
        # Count number of cars in positions[] array and add 1 delay for each
        pass
