#Алгоритм  XOR-2 с перегородкой
import sys,os,pygame,pygame_gui,itertools,random
from collections import deque
from math import tan,pi,fabs,atan2,sin,cos,copysign,sqrt
from functools import partial
from turtle import back, width
sign = partial(copysign, 1)
def chsign(val:float):return -val
from pygame import draw,display,time,quit,init,freetype,font
from pygame_gui.core import UIElement
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


def set_rect(x,y,xs,ys):
        return pygame.Rect(ToWorldCoords((DIS_WIDTH/2-x, DIS_HEIGHT/2-y)), (xs, ys))
def set_slider(x,y,xs=250,ys=25,sv=-DIS_WIDTH/2+1,ev=DIS_WIDTH/2-1,dv=0):
    return pygame_gui.elements.UIHorizontalSlider(
        relative_rect = set_rect(x,y,xs,ys),value_range=[sv,ev],start_value=dv,manager=manager)
def set_textbox(x,y,xs=50,ys=25):
    return pygame_gui.elements.UITextEntryLine(relative_rect = set_rect(x,y,xs,ys),manager=manager)
def set_button(t,x,y,xs=300,ys=25):
    return pygame_gui.elements.UIButton(relative_rect=set_rect(x,y,xs,ys),text=t,manager=manager)
def init_ui() -> dict[str,UIElement]:
    ui:dict[str,UIElement] = {
        "DRAW_POINTS":set_button('нарисовать точки',300,0),
        "DRAW_CONVEX":set_button('выпуклая оболочка',300,25),
    }
    ui["DRAW_CONVEX"].hide()
    return ui

def chain_ui():
    def tb_n_sl(sl,tb,v):
        all_ui_elements[sl].set_current_value(float(v))
        all_ui_elements[tb].set_text(str(v))

def calc_conv(pts):
    pts = pts()
    deck = []
    def foo(x,y,z):return (z[0] - x[0]) * (y[1] - x[1]) - (z[1] - x[1]) * (y[0] - x[0])
    if foo(pts[0],pts[1],pts[2])>0:
        deck.append(pts[0])
        deck.append(pts[1])
    else:
        deck.append(pts[1])
        deck.append(pts[0])
    deck.append(pts[2])
    deck.insert(0,pts[2])
    cnt = 1
    for v in pts[3:]:
        if cnt == step:break
        cnt+=1
        if foo(v,deck[-1],deck[-2])>0 or foo(deck[1],deck[0],v)>0:
            while(foo(deck[1],deck[0],v)>0):deck.pop(0)
            deck.insert(0,v)
            while(foo(v,deck[-1],deck[-2])>0):deck.pop()
            deck.append(v)
        
                        
    return deck

def draw_vect_convex(dis,col,points):
    draw.polygon(dis,col,points(),width=1)

def draw_vect_point(dis,col,coord):
    draw.circle(dis,col,coord,radius=3)

init()
manager = pygame_gui.UIManager((DIS_WIDTH, DIS_HEIGHT))
window_surface=display.set_mode((DIS_WIDTH,DIS_HEIGHT))
background = pygame.Surface((DIS_WIDTH, DIS_HEIGHT))
clock = time.Clock()
game_over=False
time_delta = 0
all_ui_elements = init_ui()
render_pipe:list[dict] = []
polygon_coords = [0,0]
points = []
step = 0

render_pipe.append({})#0 layer
render_pipe.append({})#1 layer
render_pipe.append({})#2 layer
render_pipe.append({})#3 layer
render_pipe.append({})#4 layer


render_pipe[1].update({"decart":partial(decart)})




while not game_over:
    background.fill(0)
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == all_ui_elements["OXPC"]:
                polygon_coords[0] = int(event.value)
            if event.ui_element == all_ui_elements["OYPC"]:
                polygon_coords[1] = int(event.value)

                
        if event.type == pygame.USEREVENT:
            step += 1
            if step + 3 > points.__len__():
                step = 0

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == all_ui_elements["DRAW_POINTS"]:
                step = 0
                render_pipe[3].clear()
                points.clear()
                for i in range(12):
                    p =[
                        random.randint(-DIS_WIDTH/2 + 150,DIS_WIDTH/2 - 150),
                        random.randint(-DIS_HEIGHT/2 + 150,DIS_HEIGHT/2 - 150)
                    ]
                    points.append(p)
                    render_pipe[3].update({f"draw.point{i}":partial(
                                draw_vect_point,background,GREEN,ToWorldCoords(p))})
                    points.sort(key=lambda k:k[0])
                all_ui_elements["DRAW_CONVEX"].show()

                pygame.time.set_timer(pygame.USEREVENT, 200)
                 


            if event.ui_element == all_ui_elements["DRAW_CONVEX"]:
                render_pipe[2].clear()
                def conv(f=True):
                    return [ToWorldCoords(p) for p in points] if f else points
                render_pipe[2].update({"draw.polygon":partial(
                                draw_vect_convex,background,RED,
                                partial(
                                    calc_conv,
                                    partial(
                                        conv,
                                        f=True
                                        )
                                    )
                                )})
                step += 1
                if step + 3 > points.__len__():
                    step = 0
                
                
                
            
        
                
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

