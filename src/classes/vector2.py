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
    
    @property
    def slope(self):
        return self.y / self.x

    def normalized(self):
        return self / self.magnitude
    
    def orthogonal(self):
        return Vector2(-self.y, self.x)
    
    def intify(self):
        return Vector2(int(self.x), int(self.y))
    
    def abs(self):
        return Vector2(abs(self.x), abs(self.y))
    
    def rotate(self, degrees):
        rads = math.radians(degrees)
        return Vector2(self.x * math.cos(rads) - self.y * math.sin(rads), self.y * math.cos(rads) + self.x * math.sin(rads))

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
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    @staticmethod
    def Dot(a, b):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def Angle(a, b):
        return math.acos(Vector2.Dot(a,b) / (a.magnitude * b.magnitude))