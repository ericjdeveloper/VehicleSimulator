import math

class Vector2:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def to_list(self):
        return (self.x, self.y)
    
    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        return self / self.magnitude
    
    def orthogonal(self):
        return Vector2(-self.y, self.x)

    def __str__(self):
        return f"({self.x},{self.y})"
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y) 
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        if other is 0:
            raise ZeroDivisionError
        else:
            return Vector2(self.x / other, self.y / other)
        
    def __neg__(self):
        return Vector2(-self.x, -self.y)