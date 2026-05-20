import math
import matplotlib.pyplot as plt

def calculate_failure_probability(failure_rate, time_hours):
    reliability = math.exp(-failure_rate * time_hours)
    return 1 - reliability

def generate_probability_data(failure_rate, max_hours, step):
    times = list(range(0, max_hours + step, step))
    probabilities = [calculate_failure_probability(failure_rate, t) for t in times]
    return times, probabilities
