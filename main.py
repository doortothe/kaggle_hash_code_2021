# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from classes import Simulation


sim = Simulation.read_input('test_sim.txt')
sim.read_submission('test_sched.txt')

# Run simulation
sim.run_simulation()
# Expected outcome: there should only be 1 intersections: 1
# Intersections 0 and 2 are always green