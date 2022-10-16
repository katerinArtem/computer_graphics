
import numpy as np

class Point:
    def __init__(self,x:float,y:float,z:float = 0):
        self.arr = np.array([x,y,z])
        self.x = x
        self.y = y
        self.z = z
    def __mul__(self,other:"Point")->"Point":return self.arr*other.arr
    def __sub__(self,other:"Point")->"Point":return self.arr-other.arr
    def __add__(self,other:"Point")->"Point":return self.arr+other.arr

class Line:
    def __init__(self,A:Point = None,B:Point = None,a:float = None,b:float = None):
        self.a = a
        self.b = b
        if A != None and B != None and (A.x-B.x) != 0:
            self.a = (A.y - B.y)/(A.x-B.x)
            self.b = A.y - self.a*A.x

class Plane:
    def __init__(self,a:float,b:float,c:float,d:float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
class Vector:
    def __init__(self,A:Point,B:Point):
        self.A = A
        self.B = B
        self.C = Point(B.x-A.x,B.y-A.y,B.z-A.z)
        self.len = np.sqrt(self.C.x**2+self.C.y**2+self.C.z**2)

    def nvect(self) -> "Vector":
        return Vector(Point(0,0),Point(self.B.x/self.len,self.B.y/self.len,self.B.z/self.len))

    def smul(self,other:"Vector")->float:
        return self.C.arr.dot(other.C.arr)/(self.len*other.len)

    def psmul(self,other:"Vector")->float:
        return np.linalg.det([[self.C.x,self.C.y],[other.C.x,other.C.y]])

#Лабораторная 1
#Вариант 4

#1)На плоскости Определить принадлежит ли точка прямой. Прямая задана своими коэффициентами.
def isPointOnLine(l:Line,p:Point):return p.y == l.a*p.x+l.b

#2)На плоскости Даны три точки А,В,С. Определить принадлежит ли точка С лучу АВ
def isPointOnRay(A:Point,B:Point,C:Point):return isPointOnLine(Line(A,B),C)    

#3)В пространстве Даны три точки А,В,С, определить является ли обход А-В-С обходом по часовой стрелке или против (точки заданы на плоскости).
def isRightRotation(A:Point,B:Point,C:Point):return Vector(A,B).psmul(Vector(B,C)) < 0   

#4)В пространстве Заданы коэффициенты уравнения плоскости и координаты точки. Определить принадлежит ли точка плоскости.
def isPointOnPlane(P:Plane,A:Point):return P.a*A.x + P.b*A.y + P.c*A.z + P.d == 0


print("--------isPointOnLine(Line(1,0),Point(2,2))---------------------")
print(isPointOnLine(Line(a=1,b=0),Point(2,2)))

print("--------isPointOnRay(Point(0,0),Point(1,1),Point(3,3))----------")
print(isPointOnRay(Point(0,0),Point(1,1),Point(3,3)))

print("--------isRightRotation(Point(1,1),Point(1,2),Point(0,0))-------")
print(isRightRotation(Point(1,1),Point(1,2),Point(0,0)))

print("--------isPointOnPlane(Plane(1,1,0,0),Point(0,0,1))-------------")
print(isPointOnPlane(Plane(1,1,0,0),Point(0,0,1)))


