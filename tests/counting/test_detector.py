import pytest
from core.counting.models import Point, Line
from core.counting.detector import LineCrossDetector

def test_intersection_true():
    """Test standard intersection crossing."""
    virtual_line = Line(start=Point(0, 10), end=Point(10, 10))
    trajectory = Line(start=Point(5, 5), end=Point(5, 15))
    
    intersects, direction = LineCrossDetector.check_crossing(virtual_line, trajectory)
    assert intersects is True
    # Moving from (5,5) to (5,15) crosses the line (0,10)->(10,10)
    # Vector A: (10, 0)
    # Vector B: (0, 10)
    # Cross product A x B: (10*10) - (0*0) = 100 (Positive -> In)
    assert direction == "IN"

def test_intersection_false_parallel():
    """Test lines that are parallel."""
    virtual_line = Line(start=Point(0, 10), end=Point(10, 10))
    trajectory = Line(start=Point(0, 5), end=Point(10, 5))
    
    intersects, _ = LineCrossDetector.check_crossing(virtual_line, trajectory)
    assert intersects is False

def test_intersection_false_out_of_bounds():
    """Test line segments that would intersect if infinite, but don't as segments."""
    virtual_line = Line(start=Point(0, 10), end=Point(10, 10))
    # Same slope as crossing, but too far right
    trajectory = Line(start=Point(15, 5), end=Point(15, 15))
    
    intersects, _ = LineCrossDetector.check_crossing(virtual_line, trajectory)
    assert intersects is False

def test_direction_out():
    """Test crossing in the opposite direction."""
    virtual_line = Line(start=Point(0, 10), end=Point(10, 10))
    # Moving from y=15 down to y=5
    trajectory = Line(start=Point(5, 15), end=Point(5, 5))
    
    intersects, direction = LineCrossDetector.check_crossing(virtual_line, trajectory)
    assert intersects is True
    assert direction == "OUT"
