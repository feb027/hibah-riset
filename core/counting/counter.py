from core.counting.models import Line, Point, TrackedObject, TrackState
from core.counting.detector import LineCrossDetector

class PeopleCounter:
    """Manages tracking history and counts people crossing a virtual line using a robust State Machine."""

    def __init__(self, virtual_line: Line, cooldown_threshold: int = 30) -> None:
        """Initialize the counter with debouncing mechanism.
        
        Args:
            virtual_line: The predefined boundary line.
            cooldown_threshold: Number of frames an ID must wait before being able to be counted again.
        """
        self.virtual_line = virtual_line
        self.cooldown_threshold = cooldown_threshold
        self.count_in = 0
        self.count_out = 0
        
        # State management
        self._tracks: dict[int, TrackedObject] = {}

    def update(self, track_id: int, current_centroid: Point) -> None:
        """Update the position of a tracked object, advancing its state machine.
        
        Args:
            track_id: Unique identifier for the object.
            current_centroid: Current coordinate of the object's centroid.
        """
        if track_id not in self._tracks:
            self._tracks[track_id] = TrackedObject(id=track_id)
            
        track = self._tracks[track_id]
        
        # Simpan lintasan, batasi 10 titik agar RAM tidak bocor
        track.history.append(current_centroid)
        if len(track.history) > 10:
            track.history.pop(0)
            
        if len(track.history) < 2:
            return
            
        # 1. State: COOLDOWN (Debouncing)
        # Jika baru saja dihitung, ia harus menunggu N-frame sebelum boleh dihitung lagi
        if track.state == TrackState.COOLDOWN:
            track.cooldown_frames -= 1
            if track.cooldown_frames <= 0:
                track.state = TrackState.TRACKING
            return
            
        # 2. State: TRACKING / COUNTED (Evaluasi Lintasan)
        previous_centroid = track.history[-2]
        trajectory = Line(start=previous_centroid, end=current_centroid)
        
        intersects, direction = LineCrossDetector.check_crossing(self.virtual_line, trajectory)
        
        if intersects:
            if direction == "IN":
                self.count_in += 1
            elif direction == "OUT":
                self.count_out += 1
                
            # Setelah memotong garis, paksa masuk ke masa pendinginan (Cooldown)
            track.state = TrackState.COOLDOWN
            track.cooldown_frames = self.cooldown_threshold
