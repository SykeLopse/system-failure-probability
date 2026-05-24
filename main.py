import argparse
import csv
import json
import math
import logging
import os
import statistics
from datetime import datetime
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt

# ==========================================
# SYSTEM FAILURE PROBABILITY FORECASTER V3.0
# Enterprise Grade Predictive Analytics
# ==========================================

class ConfigurationError(Exception):
    """Custom exception raised for invalid system configurations."""
    pass

class SystemConfig:
    """Enterprise configuration management for the forecasting tool."""
    def __init__(self, hours: int, rate: float, step: int):
        self.hours = hours
        self.rate = rate
        self.step = step
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.validate_config()

    def validate_config(self):
        """Ensures all baseline parameters are mathematically sound."""
        if self.hours <= 0:
            raise ConfigurationError("Total simulation hours must be greater than zero.")
        if self.rate < 0:
            raise ConfigurationError("System degradation rate (lambda) cannot be negative.")
        if self.step <= 0 or self.step > self.hours:
            raise ConfigurationError("Step size must be a positive integer smaller than total hours.")

def setup_logger(verbose: bool) -> logging.Logger:
    """Configures the standard corporate logging format with timestamps."""
    logger = logging.getLogger("FailureForecast")
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
    return logger

class HardwareComponent:
    """Represents a specific physical component within the system architecture."""
    def __init__(self, name: str, lambda_rate: float):
        self.name = name
        self.lambda_rate = lambda_rate
        self.mtbf = 1 / lambda_rate if lambda_rate > 0 else float('inf')

    def to_dict(self) -> Dict[str, Any]:
        """Serializes hardware data for JSON export."""
        return {
            "component_name": self.name,
            "failure_rate": self.lambda_rate,
            "mean_time_between_failures": self.mtbf
        }

class ReliabilityEngine:
    """Core mathematical engine for calculating degradation and failure modes."""
    def __init__(self, config: SystemConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.primary_system = HardwareComponent("Core Processing Unit", config.rate)

    def calculate_probability(self, time_interval: int) -> float:
        """
        Calculates the cumulative distribution function for exponential failure.
        Formula: F(t) = 1 - e^(-lambda * t)
        """
        try:
            return 1.0 - math.exp(-self.config.rate * time_interval)
        except OverflowError:
            self.logger.error(f"Math Engine Overflow at T={time_interval}")
            return 1.0
        except Exception as e:
            self.logger.error(f"Math Engine Error at T={time_interval}: {e}")
            return 0.0

    def generate_series(self) -> Tuple[List[int], List[float], List[float]]:
        """Generates the full timeline series for graphing and analytical export."""
        self.logger.debug("Generating timeline sequences and processing floating points...")
        time_data = list(range(0, self.config.hours + 1, self.config.step))
        prob_data = []
        rel_data = []

        for t in time_data:
            p_fail = self.calculate_probability(t)
            prob_data.append(p_fail)
            rel_data.append(1.0 - p_fail)

        self.logger.info(f"Successfully generated {len(time_data)} discrete data points.")
        return time_data, prob_data, rel_data

    def calculate_statistics(self, prob_data: List[float]) -> Dict[str, float]:
        """Calculates advanced metrics and variance on the probability dataset."""
        return {
            "mean_probability": statistics.mean(prob_data),
            "median_probability": statistics.median(prob_data),
            "variance": statistics.variance(prob_data) if len(prob_data) > 1 else 0.0,
            "stdev": statistics.stdev(prob_data) if len(prob_data) > 1 else 0.0,
            "mtbf_hours": self.primary_system.mtbf
        }

class DataExporter:
    """Handles all File I/O operations for saving simulation results to disk."""
    
    @staticmethod
    def to_csv(time_data: List[int], prob_data: List[float], rel_data: List[float], run_id: str, logger: logging.Logger):
        """Compiles the raw numerical arrays into a stakeholder-ready CSV file."""
        filename = f"export_csv_{run_id}.csv"
        logger.info(f"Initializing CSV export to {filename}...")
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time_Hours", "Failure_Probability", "System_Reliability"])
                for t, p, r in zip(time_data, prob_data, rel_data):
                    writer.writerow([t, round(p, 6), round(r, 6)])
            logger.info("CSV Export completed successfully.")
        except IOError as e:
            logger.error(f"Failed to write CSV: {e}")

class VisualizationEngine:
    """Manages the Matplotlib canvas, DPI scaling, and dual-axis rendering logic."""
    
    @staticmethod
    def plot_metrics(time_data: List[int], prob_data: List[float], rel_data: List[float], logger: logging.Logger):
        logger.info("Rendering high-resolution Matplotlib system visualizations...")
        
        plt.style.use('bmh')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=120)

        # Left Subplot: Cumulative Failure Risk
        ax1.plot(time_data, prob_data, color='#d62728', linewidth=2.5, marker='o', markersize=4, label="Cumulative Risk")
        ax1.fill_between(time_data, prob_data, color='#d62728', alpha=0.15)
        ax1.set_title("System Failure Probability Forecast", fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel("Operational Time (Hours)", fontsize=11, fontweight='semibold')
        ax1.set_ylabel("Probability of Failure (0.0 to 1.0)", fontsize=11, fontweight='semibold')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc="upper left", fontsize=10)

        # Right Subplot: System Reliability Decay
        ax2.plot(time_data, rel_data, color='#2ca02c', linewidth=2.5, marker='s', markersize=4, label="Remaining Reliability")
        ax2.fill_between(time_data, rel_data, color='#2ca02c', alpha=0.15)
        ax2.set_title("System Reliability Decay Curve", fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel("Operational Time (Hours)", fontsize=11, fontweight='semibold')
        ax2.set_ylabel("Reliability Quotient", fontsize=11, fontweight='semibold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend(loc="upper right", fontsize=10)

        plt.tight_layout(pad=3.0)
        logger.info("Displaying rendered UI plot to user...")
        plt.show()

def parse_cli_arguments() -> argparse.Namespace:
    """Constructs the command line interface options for dynamic execution."""
    parser = argparse.ArgumentParser(
        description="Enterprise System Failure Probability Forecaster V3.0",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--hours', type=int, default=1500, help="Total operational hours to simulate.")
    parser.add_argument('--rate', type=float, default=0.0025, help="System degradation rate (lambda constant).")
    parser.add_argument('--step', type=int, default=50, help="Time interval step size in hours.")
    parser.add_argument('--export', action='store_true', help="Export raw results to CSV.")
    parser.add_argument('--verbose', action='store_true', help="Enable detailed debug logging output.")
    return parser.parse_args()

def main():
    """Main execution wrapper to initialize modules and catch top-level exceptions."""
    args = parse_cli_arguments()
    logger = setup_logger(args.verbose)
    
    logger.info("=" * 60)
    logger.info("🚀 SYSTEM FAILURE PROBABILITY FORECASTER BOOTING")
    logger.info("=" * 60)
    
    try:
        config = SystemConfig(hours=args.hours, rate=args.rate, step=args.step)
        logger.debug(f"Configuration Loaded: {config.hours}h, rate={config.rate}, step={config.step}")
        
        engine = ReliabilityEngine(config, logger)
        time_series, prob_series, rel_series = engine.generate_series()
        sys_stats = engine.calculate_statistics(prob_series)
        
        if args.export:
            DataExporter.to_csv(time_series, prob_series, rel_series, config.run_id, logger)
            
        VisualizationEngine.plot_metrics(time_series, prob_series, rel_series, logger)
        
        logger.info("Simulation matrix complete. Graceful exit.")
        
    except ConfigurationError as ce:
        logger.error(f"Initialization Aborted: {ce}")
    except KeyboardInterrupt:
        logger.warning("Simulation forcefully aborted by user.")
    except Exception as e:
        logger.critical(f"Fatal System Error encountered: {e}")

if __name__ == "__main__":
    main()
