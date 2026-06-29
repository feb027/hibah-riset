import pytest
from core.counting.models import Point, Line
from core.counting.counter import PeopleCounter

@pytest.fixture
def counter():
    # Virtual line from x=0 to x=10 at y=10
    virtual_line = Line(start=Point(0, 10), end=Point(10, 10))
    # Set cooldown to 3 untuk kemudahan testing
    return PeopleCounter(virtual_line, cooldown_threshold=3)

def test_counter_registers_new_track(counter):
    """Test that a new track doesn't immediately increment count."""
    counter.update(track_id=1, current_centroid=Point(5, 5))
    
    assert counter.count_in == 0
    assert counter.count_out == 0
    assert 1 in counter._tracks

def test_counter_increments_in_count(counter):
    """Test that crossing the line in positive direction increments IN."""
    # Frame 1: Before line
    counter.update(track_id=1, current_centroid=Point(5, 5))
    # Frame 2: After line
    counter.update(track_id=1, current_centroid=Point(5, 15))
    
    assert counter.count_in == 1
    assert counter.count_out == 0

def test_counter_increments_out_count(counter):
    """Test that crossing the line in negative direction increments OUT."""
    # Frame 1: Before line (above)
    counter.update(track_id=2, current_centroid=Point(5, 15))
    # Frame 2: After line (below)
    counter.update(track_id=2, current_centroid=Point(5, 5))
    
    assert counter.count_in == 0
    assert counter.count_out == 1

def test_counter_debouncing_prevents_rapid_double_counting(counter):
    """Test that Cooldown state prevents rapid double counting."""
    # Frame 1: Mulai
    counter.update(track_id=3, current_centroid=Point(5, 5))
    # Frame 2: Menyeberang masuk (Dihitung IN, Cooldown diset = 3)
    counter.update(track_id=3, current_centroid=Point(5, 15)) 
    assert counter.count_in == 1
    
    # Frame 3-5: Mondar-mandir dalam masa Cooldown (Tidak Dihitung!)
    counter.update(track_id=3, current_centroid=Point(5, 5))  # Cooldown = 2
    counter.update(track_id=3, current_centroid=Point(5, 15)) # Cooldown = 1
    counter.update(track_id=3, current_centroid=Point(5, 5))  # Cooldown = 0 -> Kembali ke TRACKING
    
    # Angka tidak boleh bertambah selama mondar-mandir tadi
    assert counter.count_out == 0
    assert counter.count_in == 1
    
    # Frame 6: Menyeberang lagi setelah Cooldown habis (Dihitung IN lagi)
    counter.update(track_id=3, current_centroid=Point(5, 15)) 
    assert counter.count_in == 2
