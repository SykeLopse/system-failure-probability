import math
import matplotlib.pyplot as plt

def calculate_failure_probability(failure_rate, time_hours):
    reliability = math.exp(-failure_rate * time_hours)
    return 1 - reliability
