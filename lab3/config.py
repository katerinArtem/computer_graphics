import os
import sys

RED = (255,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (195, 195, 195)
LIGHT_BLUE = (0, 0, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)


PIXS_WIDTH = 48
PIXS_HEIGHT = 48
PIX_SIZE = 20

DIS_WIDTH = PIXS_WIDTH*PIX_SIZE 
DIS_HEIGHT = PIXS_HEIGHT*PIX_SIZE

#DIS_WIDTH +=  
#DIS_HEIGHT += 



def WorldToPix(coord)->list[int,int]:
    return [int((coord[0]+DIS_WIDTH/2)//PIX_SIZE),int((coord[1]+DIS_HEIGHT/2)//PIX_SIZE)]

def PixToWorld(coord):
    return [coord[0]*PIX_SIZE-DIS_WIDTH/2,coord[1]*PIX_SIZE-DIS_HEIGHT/2]

#переход к координатам локальной сетки
def ToWorldCoords(coord):
    return [coord[0]+DIS_WIDTH/2,-coord[1]+DIS_HEIGHT/2]



#возврат к координатам pygame
def ToScreenCoords(coord):
    return [coord[0]-DIS_WIDTH/2,coord[1]-DIS_HEIGHT/2]

if __name__ == "__main__":
    exec(open(f'{os.getcwd()}\\lab3\\main.py','r',encoding='UTF-8').read())