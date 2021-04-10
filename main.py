# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from classes import Simulation


sim = Simulation.read_input('test_sim.txt')
sim.read_submission('test_sched.txt')

# Run simulation
sim.run_simulation()
"""
Expected outcome:
tick 0: rue-d-athenes is green. rue-d-amsterdam is red
tick 1: rue-d-athenes is green. rue-d-amsterdam is red
tick 2: rue-d-athenes is red. rue-d-amsterdam is green
tick 3: rue-d-athenes is green. rue-d-amsterdam is red
tick 4: rue-d-athenes is green. rue-d-amsterdam is red
tick 5: rue-d-athenes is red. rue-d-amsterdam is green
"""
