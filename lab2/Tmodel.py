import pygame
from pygame import \
    draw,display,time,\
    quit,init,\
    freetype,font
import numpy as np
from math import sin,cos,pi,ceil,sqrt
from config import *

class MovableModel:
    def __init__(self,model:list[list],pos = [0,0],speed = 1,col = 200):
        self.model = [[i[0]+pos[0],i[1]-pos[1]] for i in model]
        self.spd = speed
        self.pos:list[float,float] = pos
        self.a = 0
        self.sa = 0
        self.sx = 1
        self.sy = 1
        self.col = col
        self.lounch_time = 0
        self.d_time = 0
        self.ds = 0
        self.dv = 0
        self.da = 0
        self.TM = [
                [1,0,0],
                [0,1,0],
                [pos[0],pos[1],1]
            ]
        self.RM = [
            [1,0],
            [0,1]
        ]

    def update(self):
        if self.lounch_time < 3.2 and self.d_time != 0:
            self.lounch_time += self.d_time
            self.dv = 2*sqrt(-self.lounch_time+3.5)
            self.transform([self.pos[0],self.pos[1] + self.dv])
            self.scale(1/(self.lounch_time+1),1/(self.lounch_time+1))
        else:
            self.d_time = 0
            self.dv = 0
            self.lounch_time = 0
        
        

    #применение матрицы трансформации 
    def apply_matrix(self,M):
        new_pos = np.array(M).dot(np.array([self.pos[0],self.pos[1],1]))
        self.pos = [new_pos[0],new_pos[1]]
        for i in range(len(self.model)):
            new_point = np.array(M).dot(np.array(self.model[i] + [1]))
            self.model[i] = [new_point[0],new_point[1]]

    #применение импульса поворота и движение по оси *взгляда*
    def move(self,angle = 0,dv = 0):
        if angle+dv == 0:return
        while self.a > 2*pi:self.a -= 2*pi
        while self.a < -2*pi:self.a += 2*pi 
        angle *= pi/180
        self.a += angle
        s = sin(angle)
        c = cos(angle)
        dx = self.pos[0]
        dy = self.pos[1]
        self.RM =np.array([
            [c ,s ,0],
            [-s ,c ,0],
            [-dx*(c-1)+dy*(s) ,-dx*(s)-dy*(c-1) ,1]
        ])
        self.TM = np.array([
            [1,0,dv*cos(self.a)],
            [0,1,dv*sin(self.a)],
            [0,0,1]
        ])
        self.apply_matrix(self.TM)
        self.apply_matrix(self.RM)

    #мосштабирование в локальном пространстве модели
    def scale(self,sx:float,sy:float):
        #матрица перехода к новому масштабированию
        SM = np.array([
            [sx/self.sx ,0 ,0],
            [0 ,sy/self.sy ,0],
            [0 ,0 ,1]
        ])
        old_pos = self.pos
        old_rot = self.sa
        self.transform([0,0])
        self.rotate(0)
        self.apply_matrix(SM)
        self.transform(old_pos)
        self.rotate(old_rot)
        self.sx = sx
        self.sy = sy

    #поворот относительно точки,если не указана то вокруг себя 
    def rotate(self,angle:float,point = None):
        if point == None:point = self.pos
        d_angle =self.sa - angle  
        self.sa = angle
        while self.sa >= 360:self.sa -= 360
        while self.sa <= -360:self.sa += 360
        s = sin(d_angle*pi/180)
        c = cos(d_angle*pi/180)
        dx = point[0] 
        dy = point[1] 
        RM = np.array([
            [c,-s,-dx*c + dy*s + dx],
            [s,c,-dx*s - dy*c + dy],
            [0,0,1]
        ])#T(-x,-y)*RM*T(x,y) комбинированная матрица
        self.apply_matrix(RM)
    
    #перемещение в координаты x,y
    def transform(self,point:list[float,float] = [0,0]):
        TM = np.array([
            [1,0,point[0] - self.pos[0]],
            [0,1,point[1] - self.pos[1]],
            [0,0,1]
        ])
        self.apply_matrix(TM)
        

    def render(self,dis):
        self.update()
        #self.move(self.da,self.dv)
        #отрисовка модели
        pygame.draw.polygon(dis,self.col,[tfm(p) for p in self.model])
        #отрисовка координат позиции модели
        _font:freetype.Font = freetype.SysFont(font.get_fonts()[0],14)
        text = _font.render(f"[{ceil(self.pos[0])}:{ceil(self.pos[1])}]",fgcolor=(255, 255, 255),size=13)
        dis.blit(text[0],dest=tfm([self.pos[0],self.pos[1]]))

    
