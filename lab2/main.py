import sys
import os
from math import tan,pi,fabs,atan2,sin,cos,copysign
from functools import partial
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

from Tmodel import MovableModel 

#отрисовка координатной сетки
def decart():
    _font:freetype.Font = freetype.SysFont(font.get_fonts()[0],14)
    draw.line(background,WHITE,tfm([DIS_WIDTH/2,0]),tfm([-DIS_WIDTH/2,0]))
    draw.line(background,WHITE,tfm([0,DIS_HEIGHT/2]),tfm([0,-DIS_HEIGHT/2]))
    draw.line(background,WHITE,tfm([-DIS_WIDTH/2,-DIS_HEIGHT/2]),tfm([DIS_WIDTH/2,DIS_HEIGHT/2]))
    for x in range(-int(DIS_WIDTH/2),int(DIS_WIDTH/2),25):
        for y in range(-int(DIS_HEIGHT/2),int(DIS_HEIGHT/2),25):
            if y == 0 or x == 0:
                text = _font.render(str(x) if y == 0 else str(y), fgcolor=WHITE,size=13)
                background.blit(text[0],dest=tfm([x,y]))

    
#Вариант 12
#Написать программу, выводящую на экран взлетающую ракету. С удалением от земли ракета уменьшается.

#Реализовать с заданной совокупностью фигур 
#преобразования: 
#перенос вдоль оси OX,
#перенос вдоль оси OY,
#отражение относительно оси OX,
#отражение относительно оси OY,
#отражение относительно прямой Y=X,
#масштабирование независимо по обеим осям, 
#поворот на заданный угол относительно центра координат
#поворот на заданный угол относительно произвольной точки, указываемой в ходе выполнения программы. 
#Предусмотреть восстановление исходной позиции фигур, применение нескольких преобразований. Управление организовать через меню, кнопки и т.д.
#Начало координат должно быть расположено в центре окна. 
#Обязательно использовать матрицы 1×3 для хранения координат вершин, матрицу 3×3 преобразования, метод для умножения матриц.


def init_ui() -> dict:
    return {
        
        "OXTS":pygame_gui.elements.UIHorizontalSlider(
                relative_rect = pygame.Rect(tfm((200, 500)), (300, 25)),value_range=[-DIS_WIDTH/2,DIS_WIDTH/2],start_value=0,manager=manager),
        "OXTSTB":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((150, 500)), (50, 25)),manager=manager),
        "OYTS":pygame_gui.elements.UIHorizontalSlider(
                relative_rect = pygame.Rect(tfm((200, 475)), (300, 25)),value_range=[-DIS_HEIGHT/2,DIS_HEIGHT/2],start_value=0,manager=manager),
        "OYTSTB":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((150, 475)), (50, 25)),manager=manager),
        "OXR":pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(tfm((200, 450)), (300, 25)),text='отражение относительно оси OX',manager=manager),
        "OYR":pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(tfm((200, 425)), (300, 25)),text='отражение относительно оси OY',manager=manager),
        "YXR":pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(tfm((200, 400)), (300, 25)),text='отражение относительно прямой Y=X',manager=manager),
        "OXS":pygame_gui.elements.UIHorizontalSlider(
                relative_rect = pygame.Rect(tfm((200, 375)), (300, 25)),value_range=[0,18],start_value=9,manager=manager),
        "OXSTB":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((150, 375)), (50, 25)),manager=manager),
        "OYS":pygame_gui.elements.UIHorizontalSlider(
                relative_rect = pygame.Rect(tfm((200, 350)), (300, 25)),value_range=[0,18],start_value=9,manager=manager),
        "OYSTB":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((150, 350)), (50, 25)),manager=manager),
        "OOR":pygame_gui.elements.UIHorizontalSlider(
                relative_rect = pygame.Rect(tfm((200, 325)), (300, 25)),value_range=[-180,180],start_value=90,manager=manager),
        "OORTB":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((150, 325)), (50, 25)),manager=manager),
        "SPX":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((200, 300)), (150, 25)),manager=manager),
        "SPY":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((350, 300)), (150, 25)),manager=manager),
        "PPR":pygame_gui.elements.UIHorizontalSlider(
                relative_rect = pygame.Rect(tfm((200, 275)), (300, 25)),value_range=[-180,180],start_value=90,manager=manager),
        "PPRTB":pygame_gui.elements.UITextEntryLine(
                relative_rect = pygame.Rect(tfm((150, 275)), (50, 25)),manager=manager),
        "LAUNCH_BUTTON":pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(tfm((200, 250)), (300, 25)),text='запустить ракету',manager=manager),
        "RESET_BUTTON":pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(tfm((200, 225)), (300, 25)),text='восстановить изначальное положение',manager=manager)
    }

def chain_ui():
    

    all_ui_elements["OXTS"].set_current_value(Obj.pos[0])
    all_ui_elements["OYTS"].set_current_value(Obj.pos[1])

    all_ui_elements["OXTSTB"].set_text(str(Obj.pos[0]))
    all_ui_elements["OYTSTB"].set_text(str(Obj.pos[1]))
   
    all_ui_elements["OXSTB"].set_text(str(Obj.sx))
    all_ui_elements["OYSTB"].set_text(str(Obj.sy))

    try:all_ui_elements["PPRTB"].set_text(str(atan2((Obj.pos[1] - Pobj.pos[1]),(Obj.pos[0] - Pobj.pos[0] ))*180/pi))
    except :pass
    try:all_ui_elements["OORTB"].set_text(str(atan2(Obj.pos[1],Obj.pos[0])*180/pi))
    except :pass

init()
manager = pygame_gui.UIManager((DIS_WIDTH, DIS_HEIGHT))
window_surface=display.set_mode((DIS_WIDTH,DIS_HEIGHT))
background = pygame.Surface((DIS_WIDTH, DIS_HEIGHT))
clock = time.Clock()
game_over=False
time_delta = 0
all_ui_elements = init_ui()
Obj = MovableModel(MODEL,[0,0])
Pobj = MovableModel([[5,5],[5,-5],[-5,-5],[-5,5]],[0,0],col=PINK)

launch_start = 0

while not game_over:
    background.fill(0)
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == all_ui_elements["SPX"]:
                try:Pobj.transform([float(event.text),Pobj.pos[1]])
                except :pass
            if event.ui_element == all_ui_elements["SPY"]:
                try:Pobj.transform([Pobj.pos[0],float(event.text)])
                except :pass

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            #перенос вдоль оси OX
            if event.ui_element == all_ui_elements["OXTS"]:Obj.transform([event.value,Obj.pos[1]])
            #перенос вдоль оси OY
            if event.ui_element == all_ui_elements["OYTS"]:Obj.transform([Obj.pos[0],event.value])
                
            #масштабирование независимо по обеим осям
            if event.ui_element == all_ui_elements["OXS"]:Obj.scale(1/(10-event.value) if event.value < 10 else event.value-8,Obj.sy)
            if event.ui_element == all_ui_elements["OYS"]:Obj.scale(Obj.sx,1/(10-event.value) if event.value < 10 else event.value-8)
            #поворот на заданный угол относительно центра координат
            if event.ui_element == all_ui_elements["OOR"]:
                Obj.rotate(event.value,[0,0])
                all_ui_elements["PPR"].set_current_value(atan2((Obj.pos[1] - Pobj.pos[1]),(Obj.pos[0] - Pobj.pos[0] ))*180/pi)
            #поворот на заданный угол относительно произвольной точки, указываемой в ходе выполнения программы.
            if event.ui_element == all_ui_elements["PPR"]:
                 Obj.rotate(event.value,Pobj.pos)
                 all_ui_elements["OOR"].set_current_value(atan2(Obj.pos[1],Obj.pos[0])*180/pi)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #запустить ракету
            if event.ui_element == all_ui_elements["LAUNCH_BUTTON"]:
                Obj.transform([-100,0])
                Obj.rotate(180)
                Obj.scale(1,1)
                Pobj.transform([0,0])
                Pobj.rotate(0)
                all_ui_elements["SPX"].set_text(str(Pobj.pos[0]))
                all_ui_elements["SPY"].set_text(str(Pobj.pos[1]))
                Obj.d_time = time_delta
    
            #восстановление в изначальное состояние
            if event.ui_element == all_ui_elements["RESET_BUTTON"]:
                Obj.transform([0,0])
                Obj.rotate(0)
                Obj.scale(1,1)
                Pobj.transform([0,0])
                Pobj.rotate(0)
                all_ui_elements["SPX"].set_text(str(Pobj.pos[0]))
                all_ui_elements["SPY"].set_text(str(Pobj.pos[1]))
            #отражение относительно оси OX
            if event.ui_element == all_ui_elements["OXR"]:
                Obj.transform([Obj.pos[0],-Obj.pos[1]])
                Obj.rotate(atan2(-sin(Obj.sa*pi/180),cos(Obj.sa*pi/180))*180/pi)#-sin = sin
            #отражение относительно оси OY
            if event.ui_element == all_ui_elements["OYR"]:
                Obj.transform([-Obj.pos[0],Obj.pos[1]])
                Obj.rotate(atan2(sin(Obj.sa*pi/180),-cos(Obj.sa*pi/180))*180/pi)#cos = -cos
            #отражение относительно прямой Y=X
            if event.ui_element == all_ui_elements["YXR"]:
                Obj.transform([Obj.pos[1],Obj.pos[0]])
                Obj.rotate(atan2(cos(Obj.sa*pi/180),sin(Obj.sa*pi/180))*180/pi)#cos = sin,sin = cos
            
        manager.process_events(event)
    chain_ui()
    manager.update(time_delta)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:pass
    if keys[pygame.K_RIGHT]:pass
    Obj.render(background)
    Pobj.render(background)
    decart()
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    display.update()
pygame.quit()
quit()

