# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from classes_old import Simulation


sim = Simulation.read_input('test_sim.txt')
sim.read_submission('test_sched.txt')

# Run simulation
sim.run_simulation()

# todo (debugging): debug delay tracking methods for simulation, streets, cars, and intersections
"""
Expected outcome:
tick 0: 
    car 1 crosses intersection 0 and into rue-de-amsterdam traffic
    car 2 crosses intersection 1 and into rue-de-moscou traffic
tick 1:
    car 1 crosses rue-de-amsterdam traffic and is placed in queue. 
        Can't cross due to red light
tick 2:
    car 1 can cross the street and moves to rue-de-moscou
tick 3: 
    car 2 reaches end of rue-de-moscou, is placed into queue. 
        can go because green light, into rue-de-londres
tick 4: 
    car 2 reaches end of rue-de-londres, its destination
        Scores 1002 points
tick 5: 
    car 1 reaches end of rue-de-moscou, green light, crosses to rue-de-rome
"""
