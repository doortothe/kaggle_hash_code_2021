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

    def set_cars(self, cars):
        self.cars = cars

        # set the cars into the streets where they belong
        for car in cars:
            # Find the car's current street in the sim's street array
            [street.place_car(car) for street in self.streets if street.get_id == car.get_current_streetID]

        # Debug to see if this worked
        #for street in self.streets:
            #print(street.get_id + ": " + str(street.positions))

    @classmethod
    def read_input(cls, file):
        # Read in the first line, which contains the simulation-wide variables
        f = open(file, 'r')
        line = f.readline().split(' ')

        # Instantiate the Simulation class
        sim = Simulation(int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]))

        # Create the streets
        streets = []
        for x in range(0, sim.get_num_streets):
            line = f.readline().split(' ')
            streets.append(Street(line[2], line[0], line[1], line[3]))

        # Store streets in the simulation's street array
        sim.set_streets(streets)

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
        e = int(f.readline())

        # Read through the file as specified by the first line
        for x in range(0, int(num_schedules), e):
            for y in range(0, e):


    def create_submission(self):

        # def score(self, car):
        # calculate score based on car parameters

        # If the car was removed before the simulation ended
        if self.current_time <= self.duration:
            self.score += self.points + (self.duration - self.current_time)
        # Otherwise, no score is added

        # Remove car from the simulation

    # def tick(self):
    # Check traffic light schedules

    # Move cars

    # Check if car reached its destination
    # @classmethod
    # def validate_cars():


class Car:
    destination: object

    def __init__(self, name, path):
        self.id = name
        self.path = path  # list of street ids
        self.current_street = path[0]
        self.path_index = 0
        self.destination = path[len(path) - 1]
        # self.position = None

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def cross_intersection(self):
        self.path_index += 1
        self.current_street = self.path[self.path_index]
        # Should the car check if it reached its destination, or should the simulation?
        # Should the car increment its position as it travels a street? Or the simulation?
        # What's a factory method?

    @property
    def get_current_streetID(self):
        return self.current_street

    @property
    def get_destination(self):
        return self.destination

        # def set_position(self, pos):
        # self.position = pos


class TrafficLight:
    RED = 0
    GREEN = 1

    def __init__(self, name, street):
        self.id = name
        self.state = self.RED
        self.street = street


class Intersection:

    def __init__(self, name):
        self.id = name
        self.schedule = 0
        # self.cycle_length
        self.cycle_position = 0

    def set_schedule(self, schedule):
        self.schedule = schedule


class Street:

    def __init__(self, name, start_intersection_id, end_intersection_id, length):
        self.id = name
        self.length = int(length)
        self.positions = [None] * self.length  # Initialize as empty street
        self.start_intersection_id = start_intersection_id
        self.end_intersection_id = end_intersection_id

    def place_car(self, car):
        """
        Place a car at the latest available space in the street.
        Assumes there is open space
        :return:
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