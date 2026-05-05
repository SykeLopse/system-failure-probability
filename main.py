import math

def calculate_failure_probability(time_hours, lambda_rate):
    """Calculates failure probability using the exponential distribution."""
    return 1.0 - math.exp(-lambda_rate * time_hours)

if __name__ == "__main__":
    print("--- System Failure Probability Core Logic ---")
    
    lambda_rate = 0.003
    test_hours = [0, 100, 250, 500, 750, 1000]

    print(f"Testing with Degradation Rate (Lambda) = {lambda_rate}\n")
    
    for hours in test_hours:
        prob = calculate_failure_probability(hours, lambda_rate)
        reliability = 1.0 - prob
        print(f"Hours: {hours:>4} | Failure Risk: {prob:.4f} | Remaining Reliability: {reliability:.4f}")
