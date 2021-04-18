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
