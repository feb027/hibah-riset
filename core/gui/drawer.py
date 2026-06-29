from core.counting.models import Point, Line

class LineDrawerState:
    """Manages the state of the interactive line drawing process.
    
    This class is separated from OpenCV to ensure it is unit-testable
    and follows the Single Responsibility Principle.
    """
    def __init__(self) -> None:
        self.point1: Point | None = None
        self.point2: Point | None = None

    @property
    def is_complete(self) -> bool:
        """Check if both points of the line have been drawn."""
        return self.point1 is not None and self.point2 is not None

    def add_point(self, x: int, y: int) -> None:
        """Add a point to the line state.
        
        If point1 is missing, it sets point1.
        If point1 exists but point2 is missing, it sets point2.
        If both exist, it resets and starts over with point1.
        """
        if self.is_complete:
            self.reset()
            self.point1 = Point(float(x), float(y))
        elif self.point1 is None:
            self.point1 = Point(float(x), float(y))
        else:
            self.point2 = Point(float(x), float(y))

    def reset(self) -> None:
        """Reset the drawing state."""
        self.point1 = None
        self.point2 = None

    def get_line(self) -> Line:
        """Get the constructed Line object.
        
        Raises:
            ValueError: If the line is not completely drawn.
        """
        if not self.is_complete:
            raise ValueError("Cannot get line: Drawing is incomplete. Both points must be set.")
        
        # We can assert they are not None because is_complete checked it,
        # but the type checker might need explicit confirmation.
        assert self.point1 is not None
        assert self.point2 is not None
        
        return Line(start=self.point1, end=self.point2)
