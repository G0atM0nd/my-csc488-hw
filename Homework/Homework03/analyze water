//Part 1
import json
import logging
from typing import List, Dict

# Constants
SAFE_THRESHOLD = 1.0  # NTU
DECAY_FACTOR = 0.02  # 2% per hour

def calculate_turbidity(a0: float, I90: float) -> float:
    """
    Calculate turbidity using the formula T = a0 * I90
    
    Args:
        a0 (float): Calibration constant
        I90 (float): Ninety degree detector current
        
    Returns:
        float: Turbidity in NTU units
    """
    return a0 * I90

def calculate_min_time(current_turbidity: float, threshold: float, decay: float) -> float:
    """
    Calculate the minimum time required for turbidity to fall below a safe threshold.
    
    Args:
        current_turbidity (float): Current turbidity
        threshold (float): Safe threshold for turbidity
        decay (float): Decay factor per hour
        
    Returns:
        float: Minimum time in hours to reach below the safe threshold
    """
    if current_turbidity <= threshold:
        return 0.0
    
    import math
    return math.log(threshold / current_turbidity) / math.log(1 - decay)

def main():
    # Load the data
    with open('turbidity_data.json', 'r') as f:
        data = json.load(f)
    
    # Get the most recent 5 data points
    recent_data = data['turbidity_data'][:5]
    
    # Calculate turbidity for the last 5 data points
    turbidity_values = []
    for entry in recent_data:
        T = calculate_turbidity(entry['calibration_constant'], entry['detector_current'])
        turbidity_values.append(T)
    
    # Calculate average turbidity
    avg_turbidity = sum(turbidity_values) / len(turbidity_values)
    
    # Display results
    print(f"Average turbidity based on most recent five measurements = {avg_turbidity:.4f} NTU")
    
    if avg_turbidity > SAFE_THRESHOLD:
        logging.warning("Turbidity is above threshold for safe use")
    else:
        logging.info("Turbidity is below threshold for safe use")
    
    # Calculate minimum time to fall below threshold
    min_time = calculate_min_time(avg_turbidity, SAFE_THRESHOLD, DECAY_FACTOR)
    print(f"Minimum time required to return below a safe threshold = {min_time:.2f} hours")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

// Part 2 
import pytest
from turbidity import calculate_turbidity, calculate_min_time

def test_calculate_turbidity():
    # Sanity checks
    assert calculate_turbidity(1.022, 1.137) == pytest.approx(1.161114)
    assert calculate_turbidity(0.975, 1.141) == pytest.approx(1.112475)
    
    # Edge cases
    assert calculate_turbidity(0, 1.137) == 0
    assert calculate_turbidity(1.022, 0) == 0
    assert calculate_turbidity(0, 0) == 0

def test_calculate_min_time():
    # Below threshold should return 0
    assert calculate_min_time(0.9852, 1.0, 0.02) == 0.0
    
    # Above threshold calculations
    assert calculate_min_time(1.1992, 1.0, 0.02) == pytest.approx(8.99, 0.01)
    
    # Edge cases
    assert calculate_min_time(1.0, 1.0, 0.02) == 0.0
    assert calculate_min_time(2.0, 1.0, 0.02) > 0
    
    # Type checks
    with pytest.raises(TypeError):
        calculate_min_time("string", 1.0, 0.02)
    with pytest.raises(TypeError):
        calculate_min_time(1.0, "string", 0.02)
    with pytest.raises(TypeError):
        calculate_min_time(1.0, 1.0, "string")
