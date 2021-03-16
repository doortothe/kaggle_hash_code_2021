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

    if (var_check == 'I' or var_check == 'S') and 2 <= var <= 10 ^ 5:
        return var

    if var_check == 'V' and 2 <= var <= 10 ^ 3:
        return var

    if var_check == 'F' and 1 <= var <= 10 ^ 3:
        return var

    raise Exception("Inappropriate value for " + var_check + ": " + str(var))

def validate_cars()

class Simulation:
    def __init__(self, duration, num_intersections, num_streets, num_cars, points):
        self.duration = validate_variable(duration, 'D')
        self.num_intersections = validate_variable(num_intersections, 'I')
        self.num_streets = validate_variable(num_streets, 'S')
        self.num_cars = validate_variable(num_cars, 'S')
        self.points = validate_variable(points, 'F')

        self.score = 0

    def read_input(self):


    def create_submission(self):


    def score(self, car):
        # calculate score based on car parameters

        # Remove car from the simulation

    def tick(self):

    @classmethod
    def validate_cars():


class Car:
    destination: object

    def __init__(self, path ):
        self.path = path # list of streets
        self.current_street = path[0]
        self.path_index = 0
        self.destination = path[len(path) - 1]
        self.position =

    def cross_intersection(self):
        self.path_index += 1
        self.current_street = self.path[self.path_index]
        # Should the car check if it reached its destination, or should the simulation?
        # Should the car increment its position as it travels a street? Or the simulation?
        # What's a factory method?

    @property
    def get_current_street(self):
        return self.current_street

    @property
    def get_destination(self):
        return self.destination

class TrafficLight:
    RED = 0
    GREEN = 1

    def __init__(self, name, street):
        self.id = name
        self.state = self.RED
        self.street

class Intersection:

    def __init__(self, name, schedule, street1, street2):
        self.id = name
        self.schedule = schedule
        self.cycle_length
        self.cycle_position = 0

class Street:

    def __init__(self, length):
        self.length = length
        self.positions = [None] * length # Initialize as empty street

    def place_car(self, ):
        """
        Place a car at the latest available space in the street
        :return:
        """