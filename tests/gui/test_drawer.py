import pytest
from core.counting.models import Point, Line
from core.gui.drawer import LineDrawerState

def test_initial_state():
    """Test that a new LineDrawerState is empty and incomplete."""
    state = LineDrawerState()
    assert state.point1 is None
    assert state.point2 is None
    assert not state.is_complete
    
    with pytest.raises(ValueError):
        state.get_line()

def test_add_first_point():
    """Test adding the first point sets point1."""
    state = LineDrawerState()
    state.add_point(10, 20)
    
    assert state.point1 == Point(10.0, 20.0)
    assert state.point2 is None
    assert not state.is_complete

def test_add_second_point_completes_line():
    """Test adding a second point completes the line."""
    state = LineDrawerState()
    state.add_point(10, 20)
    state.add_point(30, 40)
    
    assert state.is_complete
    line = state.get_line()
    assert isinstance(line, Line)
    assert line.start == Point(10.0, 20.0)
    assert line.end == Point(30.0, 40.0)

def test_add_third_point_resets():
    """Test adding a third point resets the state and sets it as the new first point."""
    state = LineDrawerState()
    state.add_point(10, 20)
    state.add_point(30, 40)
    assert state.is_complete
    
    # Third point should reset point2 and replace point1
    state.add_point(50, 60)
    
    assert not state.is_complete
    assert state.point1 == Point(50.0, 60.0)
    assert state.point2 is None

def test_reset_method():
    """Test manual reset works."""
    state = LineDrawerState()
    state.add_point(10, 20)
    state.reset()
    
    assert state.point1 is None
    assert not state.is_complete
