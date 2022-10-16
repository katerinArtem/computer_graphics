RED = (255,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
DIS_WIDTH = 1000
DIS_HEIGHT =1000
MODEL = [
        [15,50],
        [20,40],[30,40],
        [25,30],[30,30],
        [30,20],
        [15,0],
        [0,20],
        [0,30],[5,30],
        [0,40],[10,40],
    ]
#перемещение координат модели для центрирования позиции
MODEL = [[x[0]-15,x[1]-25] for x in MODEL]

#переход к координатам локальной сетки
def tfm(coord):return [coord[0]+DIS_WIDTH/2,-coord[1]+DIS_HEIGHT/2]

#возврат к координатам pygame
def rtfm(coord):return [coord[0]-DIS_WIDTH/2,coord[1]-DIS_HEIGHT/2]