from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

@dataclass(frozen=True)
class Point:
    """Represents a 2D coordinate in pixels."""
    x: float
    y: float

@dataclass(frozen=True)
class Line:
    """Represents a virtual line defined by two points."""
    start: Point
    end: Point

class TrackState(Enum):
    """Lifecycle states of a tracked object for robust counting."""
    UNSEEN = auto()
    TRACKING = auto()
    COUNTED_IN = auto()
    COUNTED_OUT = auto()
    COOLDOWN = auto()
    EXPIRED = auto()

@dataclass
class TrackedObject:
    """Stores the state and history of a tracked object to prevent double counting."""
    id: int
    history: List[Point] = field(default_factory=list)
    state: TrackState = TrackState.TRACKING
    cooldown_frames: int = 0
    last_updated: int = 0  # Can be frame index or timestamp


