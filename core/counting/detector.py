from core.counting.models import Line, Point

class LineCrossDetector:
    """Mathematical service to detect if a trajectory intersects a virtual line."""

    @staticmethod
    def _ccw(A: Point, B: Point, C: Point) -> bool:
        """Check if points A, B, C are in counter-clockwise order."""
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    @staticmethod
    def check_crossing(virtual_line: Line, trajectory: Line) -> tuple[bool, str | None]:
        """Check if the trajectory intersects the virtual line and determine direction.
        
        Args:
            virtual_line: The predefined boundary line.
            trajectory: The movement vector of the object from previous to current frame.
            
        Returns:
            Tuple of (intersects: bool, direction: str | None).
            Direction is "IN" or "OUT".
        """
        A = virtual_line.start
        B = virtual_line.end
        C = trajectory.start
        D = trajectory.end

        # Line intersection check
        intersects = (
            LineCrossDetector._ccw(A, C, D) != LineCrossDetector._ccw(B, C, D) and
            LineCrossDetector._ccw(A, B, C) != LineCrossDetector._ccw(A, B, D)
        )

        if not intersects:
            return False, None

        # Determine direction using 2D cross product of vectors
        # Vector A (virtual line): B - A
        vA_x = B.x - A.x
        vA_y = B.y - A.y
        
        # Vector B (trajectory): D - C
        vB_x = D.x - C.x
        vB_y = D.y - C.y
        
        # Cross product
        cross_product = (vA_x * vB_y) - (vA_y * vB_x)
        
        if cross_product > 0:
            return True, "IN"
        else:
            return True, "OUT"
