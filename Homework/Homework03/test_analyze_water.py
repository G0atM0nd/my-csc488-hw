
import pytest
from turbidity_analysis import calculate_turbidity, calculate_time_to_safe_threshold

def test_calculate_turbidity():
    """Test the calculate_turbidity function."""
    assert calculate_turbidity(1.0, 1.0) == 1.0
    assert calculate_turbidity(1.5, 2.0) == 3.0
    assert calculate_turbidity(0.0, 10.0) == 0.0
    assert calculate_turbidity(2.5, 4.0) == 10.0
    assert calculate_turbidity(1.2, -1.0) == -1.2  # Handling negative values

def test_calculate_time_to_safe_threshold():
    """Test the calculate_time_to_safe_threshold function."""
    assert calculate_time_to_safe_threshold(0.5) == 0.0  # Already safe
    assert calculate_time_to_safe_threshold(1.0) == 0.0  # Exactly at threshold
    assert calculate_time_to_safe_threshold(2.0) > 0  # Needs decay time
    assert isinstance(calculate_time_to_safe_threshold(5.0), float)  # Type check
    with pytest.raises(ValueError):
        calculate_time_to_safe_threshold(-1.0)  # Invalid turbidity input
