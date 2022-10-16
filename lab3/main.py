import sys
import os
from math import tan,pi,fabs,atan2,sin,cos,copysign
from functools import partial
from turtle import back
sign = partial(copysign, 1)
def chsign(val:float):return -val
    
import pygame
import random as rnd
from pygame import \
    draw,display,time,\
    quit,init,\
    freetype,font
import pygame_gui 
from config import *

CELL = [
    [0,0],[PIX_SIZE-2,0],[PIX_SIZE-2,PIX_SIZE-2],[0,PIX_SIZE-2]
    ]

#отрисовка координатной сетки
def decart():
    _font:freetype.Font = freetype.SysFont(font.get_fonts()[0],12)
    draw.line(background,RED,ToWorldCoords([DIS_WIDTH/2,0]),ToWorldCoords([-DIS_WIDTH/2,0]))
    draw.line(background,RED,ToWorldCoords([0 ,DIS_HEIGHT/2]),ToWorldCoords([0,-DIS_HEIGHT/2]))
    for x in range(-int(DIS_WIDTH/2),int(DIS_WIDTH/2)+PIX_SIZE,PIX_SIZE):
        for y in range(-int(DIS_HEIGHT/2),int(DIS_HEIGHT/2)+PIX_SIZE,PIX_SIZE):
            if y == 0 or x == 0:
                draw.circle(background,LIGHT_BLUE,ToWorldCoords([x,y]),1)
                text = _font.render(str(x) if y == 0 else str(y), fgcolor=LIGHT_BLUE,size=12)
                background.blit(text[0],dest=ToWorldCoords([x-9,y-5]))


class cell:
    cell_matrix:list[list["cell"]]
    def __init__(self,model,pos,width,color = GRAY):
        self.model = [[p[0]+pos[0],p[1]+pos[1]] for p in model]
        self.color = color
        self.pos = pos
        self.width = width
    def render(self):
        draw.polygon(background,self.color,[ToWorldCoords(p) for p in self.model])
        draw.circle(background,RED,ToWorldCoords([self.pos[0],self.pos[1]]),1)
    def setCell(color,pos):
        if abs(pos[0]+5) < DIS_WIDTH/2 and abs(pos[1]+5) < DIS_HEIGHT/2: 
            cell.cell_matrix[WorldToPix(pos)[0]][WorldToPix(pos)[1]].color = color
        else:print("pixel out of range")
    def render_matrix():
        for l in cell.cell_matrix:
            for c in l:c.render()
    def clear():
        for l in cell.cell_matrix:
            for c in l:c.color = GRAY
    def draw_line(A,B,color = PINK):
        A,B = WorldToPix(A),WorldToPix(B)
        if A == B :cell.setCell(color,PixToWorld(A)) 
        steep = abs(B[1]-A[1]) > abs(B[0]-A[0])
        x0,x1,y0,y1 = (A[1],B[1],A[0],B[0]) if steep else (A[0],B[0],A[1],B[1])
        dx,dy = abs(x1-x0),abs(y1-y0)
        er,der,y = 0,(dy + 1),y0
        for x in range(x0,x1+(1 if x1-x0 >= 0 else -1),1 if x1-x0 >= 0 else -1):
            cell.setCell(color,PixToWorld([y,x] if steep else [x,y]))
            er += der
            if er >= (dx + 1):
                y += (1 if y1-y0 >= 0 else -1)
                er -= (dx + 1)
    def draw_circle(A,R,color = RED):
        A,R = WorldToPix(A),WorldToPix([R[0] - DIS_WIDTH/2,0])[0]
        x,y,(x0,y0),rer = R,0,A,1 - R
        while(x >= y):
            cell.setCell(color,PixToWorld([x+x0,y+y0]));cell.setCell(color,PixToWorld([y+x0,x+y0]))
            cell.setCell(color,PixToWorld([x+x0,-y+y0]));cell.setCell(color,PixToWorld([y+x0,-x+y0]))
            cell.setCell(color,PixToWorld([-x+x0,y+y0]));cell.setCell(color,PixToWorld([-y+x0,x+y0]))
            cell.setCell(color,PixToWorld([-x+x0,-y+y0]));cell.setCell(color,PixToWorld([-y+x0,-x+y0]))
            y+=1
            if rer < 0 : rer += 2*y + 1
            else : 
                x-=1
                rer += 2*(y-x +1)

def cellMatrix() -> list:
    matrix = []
    for x in range(-int(DIS_WIDTH/2),int(DIS_WIDTH/2),PIX_SIZE):
        line = []
        for y in range(-int(DIS_HEIGHT/2),int(DIS_HEIGHT/2),PIX_SIZE):
            line.append(cell([[p[0]+1,p[1]+1] for p in CELL],[x,y],PIX_SIZE,GRAY))
        matrix.append(line)
    return matrix

def init_ui() -> dict:
    def set_rect(x,y,xs,ys):
        return pygame.Rect(ToWorldCoords((DIS_WIDTH/2-x, DIS_HEIGHT/2-y)), (xs, ys))
    def set_slider(x,y,xs=250,ys=25,sv=-DIS_WIDTH/2+5,ev=DIS_WIDTH/2-5,dv=0):
        return pygame_gui.elements.UIHorizontalSlider(
            relative_rect = set_rect(x,y,xs,ys),value_range=[sv,ev],start_value=dv,manager=manager)
    def set_textbox(x,y,xs=50,ys=25):
        return pygame_gui.elements.UITextEntryLine(relative_rect = set_rect(x,y,xs,ys),manager=manager)
    def set_button(t,x,y,xs=300,ys=25):
        return pygame_gui.elements.UIButton(relative_rect=set_rect(x,y,xs,ys),text=t,manager=manager)
    return {
        "DRAW_CIRCLE":set_button('нарисовать окружность',300,0),
        "OXCC":set_slider(300,25),"OXCCTB":set_textbox(50,25),
        "OYCC":set_slider(300,50),"OYCCTB":set_textbox(50,50),
        "CR":set_slider(300,75,sv=0,ev=DIS_WIDTH/2-10),"CRTB":set_textbox(50,75),
        "DRAW_LINE":set_button('нарисовать линию',300,100),
        "OX1LC":set_slider(300,125),"OX1LCTB":set_textbox(50,125),
        "OY1LC":set_slider(300,150),"OY1LCTB":set_textbox(50,150),
        "OX2LC":set_slider(300,175),"OX2LCTB":set_textbox(50,175),
        "OY2LC":set_slider(300,200),"OY2LCTB":set_textbox(50,200),
        "CLEAR":set_button('очистить',300,225),
    }

def chain_ui():
    def tb_n_sl(sl,tb,v):
        all_ui_elements[sl].set_current_value(float(v))
        all_ui_elements[tb].set_text(str(v))

    tb_n_sl("OXCC","OXCCTB",circle_coords[0])
    tb_n_sl("OYCC","OYCCTB",circle_coords[1])
    tb_n_sl("CR","CRTB",circle_rad[0])
    tb_n_sl("OX1LC","OX1LCTB",line_coords[0][0])
    tb_n_sl("OY1LC","OY1LCTB",line_coords[0][1])
    tb_n_sl("OX2LC","OX2LCTB",line_coords[1][0])
    tb_n_sl("OY2LC","OY2LCTB",line_coords[1][1])


def draw_vect_line(dis,color,srtp,endp):draw.line(dis,color,srtp(),endp())
def draw_vect_circle(dis,color,centr,rad):draw.circle(dis,color,centr(),rad()[0]-DIS_WIDTH/2,width=1)

init()
cell.cell_matrix = cellMatrix()
manager = pygame_gui.UIManager((DIS_WIDTH, DIS_HEIGHT))
window_surface=display.set_mode((DIS_WIDTH,DIS_HEIGHT))
background = pygame.Surface((DIS_WIDTH, DIS_HEIGHT))
clock = time.Clock()
game_over=False
time_delta = 0
all_ui_elements = init_ui()
render_pipe:list[dict] = []
line_coords = [[0,0],[0,0]]
circle_coords = [0,0]
circle_rad = [0,0]

render_pipe.append({})#0 layer
render_pipe.append({})#1 layer
render_pipe.append({})#2 layer
render_pipe.append({})#3 layer

render_pipe[2].update({"cell.render_matrix":partial(cell.render_matrix)})
render_pipe[2].update({"cell.clear":partial(cell.clear)})

render_pipe[3].update({"decart":partial(decart)})



while not game_over:
    background.fill(0)
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == all_ui_elements["OXCC"]:circle_coords[0] = int(event.value)
            if event.ui_element == all_ui_elements["OYCC"]:circle_coords[1] = int(event.value)
            if event.ui_element == all_ui_elements["CR"]:circle_rad[0] = int(event.value)

            if event.ui_element == all_ui_elements["OX1LC"]:line_coords[0][0] = int(event.value)
            if event.ui_element == all_ui_elements["OY1LC"]:line_coords[0][1] = int(event.value)
            if event.ui_element == all_ui_elements["OX2LC"]:line_coords[1][0] = int(event.value)
            if event.ui_element == all_ui_elements["OY2LC"]:line_coords[1][1] = int(event.value)
                
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == all_ui_elements["DRAW_CIRCLE"]:
                if render_pipe[0].get("cell.draw_circle") == None:
                    render_pipe[0].update({"cell.draw_circle":partial(cell.draw_circle,circle_coords,circle_rad,PINK)})
                render_pipe[3].update({"draw.circle":partial(
                            draw_vect_circle,background,GREEN,
                            partial(ToWorldCoords,circle_coords),
                            partial(ToWorldCoords,circle_rad)
                        )
                    }
                )
            if event.ui_element == all_ui_elements["DRAW_LINE"]:
                if render_pipe[0].get("cell.draw_line") == None:
                    render_pipe[0].update({"cell.draw_line":partial(
                                cell.draw_line,
                                line_coords[0],
                                line_coords[1],PINK
                            )
                        }
                    )
                render_pipe[3].update({"draw.line":partial(
                                draw_vect_line,background,GREEN,
                                partial(ToWorldCoords,line_coords[0]),
                                partial(ToWorldCoords,line_coords[1])
                            )
                        }
                    )
            if event.ui_element == all_ui_elements["CLEAR"]:
                if render_pipe[0].get("cell.draw_circle"):render_pipe[0].pop("cell.draw_circle")
                if render_pipe[3].get("draw.circle"):render_pipe[3].pop("draw.circle")

                if render_pipe[0].get("cell.draw_line"):render_pipe[0].pop("cell.draw_line")
                if render_pipe[3].get("draw.line"):render_pipe[3].pop("draw.line")
                
        manager.process_events(event)
    chain_ui()
    manager.update(time_delta)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:pass
    if keys[pygame.K_RIGHT]:pass
    
    for layer in render_pipe:
        for k in layer:layer[k]()
    
    
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    display.update()
pygame.quit()
quit()