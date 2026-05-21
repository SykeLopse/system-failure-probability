import math
import matplotlib.pyplot as plt

def calculate_failure_probability(failure_rate, time_hours):
    reliability = math.exp(-failure_rate * time_hours)
    return 1 - reliability

def generate_probability_data(failure_rate, max_hours, step):
    times = list(range(0, max_hours + step, step))
    probabilities = [calculate_failure_probability(failure_rate, t) for t in times]
    return times, probabilities

if __name__ == '__main__':
    SYSTEM_FAILURE_RATE = 0.015
    MAX_HOURS = 200
    STEP = 10
    t_data, p_data = generate_probability_data(SYSTEM_FAILURE_RATE, MAX_HOURS, STEP)
    print('Time (Hrs) | Failure Prob')
    for t, p in zip(t_data, p_data):
        print(f'{t:<11} | {p:.4f}')
