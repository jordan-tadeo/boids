

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __add__(self, v2):
        if isinstance(v2, Vector2):
            return Vector2(self.x + v2.x, self.y + v2.y)
        
    def __sub__(self, v2):
        if isinstance(v2, Vector2):
            return Vector2(self.x - v2.x, self.y - v2.y)
    
    def __mul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self
    
    def setX(self, x:float):
        self.x = x
    
    def setY(self, y:float):
        self.y = y

    def getX(self) -> float:
        return self.x
    
    def getY(self) -> float:
        return self.y