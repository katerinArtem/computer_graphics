#1. Реализовать алгоритм Цируса-Бека отсечения отрезка многоугольником. ok
#2. Реализовать алгоритм Сазерленда-Коэна. ok
#3. Реализовать алгоритм средней точки.

import sys,os,pygame,pygame_gui
from math import tan,pi,fabs,atan2,sin,cos,copysign,sqrt
from functools import partial
from turtle import back, width
sign = partial(copysign, 1)
def chsign(val:float):return -val
from pygame import draw,display,time,quit,init,freetype,font
from pygame_gui.core import UIElement
from config import *

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

def set_slider(x,y,xs=250,ys=25,sv=-DIS_WIDTH/2+5,ev=DIS_WIDTH/2-5,dv=0):
    return pygame_gui.elements.UIHorizontalSlider(
        relative_rect = set_rect(x,y,xs,ys),value_range=[sv,ev],start_value=dv,manager=manager)

def set_textbox(x,y,xs=50,ys=25):
    return pygame_gui.elements.UITextEntryLine(relative_rect = set_rect(x,y,xs,ys),manager=manager)

def set_button(t,x,y,xs=300,ys=25):
    return pygame_gui.elements.UIButton(relative_rect=set_rect(x,y,xs,ys),text=t,manager=manager)

def init_ui() -> dict[str,UIElement]:
    ui:dict[str,UIElement] = {
        "DRAW_POLYGON":set_button('нарисовать полигон',300,0),
        "DRAW_RECTANGLE":set_button('нарисовать прямоугольник',300,25),
        "OXPC":set_slider(300,50),"OXPCTB":set_textbox(50,50),
        "OYPC":set_slider(300,75),"OYPCTB":set_textbox(50,75),
        "DRAW_LINE":set_button('нарисовать отрезок',300,100),
        "OX1LC":set_slider(300,125),"OX1LCTB":set_textbox(50,125),
        "OY1LC":set_slider(300,150),"OY1LCTB":set_textbox(50,150),
        "OX2LC":set_slider(300,175),"OX2LCTB":set_textbox(50,175),
        "OY2LC":set_slider(300,200),"OY2LCTB":set_textbox(50,200),
        "CUT_LINE_1":set_button('отсечь отрезок',300,225),
        "CUT_LINE_2":set_button('отсечь отрезок 1 способом',300,225),
        "CUT_LINE_3":set_button('отсечь отрезок 2 способом',300,250),
    }
    ui["CUT_LINE_1"].hide()
    ui["CUT_LINE_2"].hide()
    ui["CUT_LINE_3"].hide()
    return ui

def chain_ui():
    def tb_n_sl(sl,tb,v):
        all_ui_elements[sl].set_current_value(float(v))
        all_ui_elements[tb].set_text(str(v))
    tb_n_sl("OXPC","OXPCTB",polygon_coords[0]);tb_n_sl("OYPC","OYPCTB",polygon_coords[1])
    tb_n_sl("OX1LC","OX1LCTB",line_coords[0][0]);tb_n_sl("OY1LC","OY1LCTB",line_coords[0][1])
    tb_n_sl("OX2LC","OX2LCTB",line_coords[1][0]);tb_n_sl("OY2LC","OY2LCTB",line_coords[1][1])

init()
manager = pygame_gui.UIManager((DIS_WIDTH, DIS_HEIGHT))
window_surface=display.set_mode((DIS_WIDTH,DIS_HEIGHT))
background = pygame.Surface((DIS_WIDTH, DIS_HEIGHT))
clock = time.Clock()
game_over=False
time_delta = 0
all_ui_elements = init_ui()
render_pipe:list[dict] = []
line_coords = [[0,0],[0,0]]
polygon_coords = [0,0]
render_pipe.append({});render_pipe.append({})
render_pipe.append({});render_pipe.append({})
render_pipe[1].update({"decart":partial(decart)})



def draw_vect_line(dis,col,srtp,endp):draw.line(dis,col,srtp(),endp())

def draw_vect_polygon(dis,col,model,cntr):
    draw.polygon(dis,col,[[x[0]+cntr()[0],-x[1]+cntr()[1]] for x in model],width=1)

def draw_cut_line_1(dis,fcol,scol,srtp,endp,model,pcntr):
    srtp,endp,pcntr = ToScreenCoords(srtp()),ToScreenCoords(endp()),ToScreenCoords(pcntr())
    polygon = [[x[0]+pcntr[0],x[1]+pcntr[1]] for x in model]
    x0,y0,t0,t1 = endp[0]-srtp[0],endp[1]-srtp[1],0,1
    for p1,p2 in zip(list(reversed(polygon)),list(reversed(polygon))[1:]+list(reversed(polygon))[:1]):
        (x1,y1),(x2,y2) = p1,p2
        nx,ny = y1-y2,x2-x1#вектор нормали к стороне
        p = nx*x0 + ny*y0#скалярное произведение векторов Dck
        wx,wy = srtp[0]-x1,srtp[1]-y1
        q = nx*wx+ny*wy#Wck
        if p != 0:
            t = -q/p
            if p  > 0 :
                if t > 1:
                    draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(endp))
                    return
                else:t0 = max(t,t0)
            else:
                if t < 0:
                    draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(endp))
                    return
                else:t1 = min(t,t1)
        else:
            if q <0:
                draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(endp))
                return
    if t0 <= t1:
        fp = [srtp[0]+t0*(endp[0]-srtp[0]),srtp[1]+t0*(endp[1]-srtp[1])]
        sp = [srtp[0]+t1*(endp[0]-srtp[0]),srtp[1]+t1*(endp[1]-srtp[1])]
        draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(fp))
        draw.line(dis,fcol,ToWorldCoords(sp),ToWorldCoords(endp))
        draw.line(dis,scol,ToWorldCoords(fp),ToWorldCoords(sp))
    else:
        draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(endp))

def draw_cut_line_2(dis,fcol,scol,srtp,endp,model,pcntr):
    srtp,endp,pcntr = ToScreenCoords(srtp()),ToScreenCoords(endp()),ToScreenCoords(pcntr())
    pol = [[x[0]+pcntr[0],x[1]+pcntr[1]] for x in model]
    x_min,y_min,x_max,y_max = pol[0][0],pol[0][1],pol[0][0],pol[0][1]
    for x,y in pol:x_min,y_min,x_max,y_max = min(x_min,x), min(y_min,y),max(x_max,x),max(y_max,y)
    def code(p):
        return  int(
            str(int(p[1] > y_max))+# 8 TOP
            str(int(p[1] < y_min))+# 4 BOT
            str(int(p[0] > x_max))+# 2 RIGHT
            str(int(p[0] < x_min)) # 1 LEFT
            ,2)

    LEFT,RIGHT,BOT,TOP = 1,2,4,8
    fp,sp,fpc,spc = srtp,endp,code(srtp),code(endp)
    print(fpc,spc)
    while(fpc | spc):
        if (fpc & spc):draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(endp));return
		# выбираем точку c с ненулевым кодом 
        nnpc,nnp = (fpc,fp) if fpc else (spc,sp)
        dx,dy = fp[0] - sp[0],fp[1] - sp[1]
        if (nnpc & LEFT):nnp = [x_min,nnp[1] + dy * (x_min - nnp[0]) / dx]
        elif (nnpc & RIGHT):nnp = [x_max,nnp[1] + dy * (x_max - nnp[0]) / dx]
        elif (nnpc & BOT):nnp = [nnp[0]+dx * (y_min - nnp[1]) / dy,y_min]
        elif (nnpc & TOP):nnp = [nnp[0]+dx * (y_max - nnp[1]) / dy,y_max]
        if (nnpc == fpc):fp,fpc = nnp,code(nnp)
        else:sp,spc = nnp,code(nnp)
    
    draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(fp))
    draw.line(dis,scol,ToWorldCoords(fp),ToWorldCoords(sp))
    draw.line(dis,fcol,ToWorldCoords(sp),ToWorldCoords(endp))

def draw_cut_line_3(dis,fcol,scol,srtp,endp,model,pcntr):
    srtp,endp,pcntr = ToScreenCoords(srtp()),ToScreenCoords(endp()),ToScreenCoords(pcntr())
    pol = [[x[0]+pcntr[0],x[1]+pcntr[1]] for x in model]
    x_min,y_min,x_max,y_max = pol[0][0],pol[0][1],pol[0][0],pol[0][1]
    for x,y in pol:x_min,y_min,x_max,y_max = min(x_min,x), min(y_min,y),max(x_max,x),max(y_max,y)
    def code(p):
        return  int(
            str(int(p[1] > y_max))+# 8 TOP
            str(int(p[1] < y_min))+# 4 BOT
            str(int(p[0] > x_max))+# 2 RIGHT
            str(int(p[0] < x_min)) # 1 LEFT
            ,2)

    ACCURACY = 10

    def check(a,b):#возвращает либо None либо две точки
        ac,bc = code(a),code(b)
        if(ac | bc):
            if(ac & bc):return None
            m = [(a[0]+b[0])/2,(a[1]+b[1])/2]
            if (abs(a[0]-b[0]) < ACCURACY) and (abs(a[1]-b[1]) < ACCURACY):return [a,b]
            amv,mbv = check(a,m),check(m,b)
            if amv != None:
                if mbv != None:return [amv[0],mbv[1]]
                else:return amv
            else:return mbv
        else:return [a,b]

    fsv = check(srtp,endp)
    if fsv != None:
        draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(fsv[0]))
        draw.line(dis,scol,ToWorldCoords(fsv[0]),ToWorldCoords(fsv[1]))
        draw.line(dis,fcol,ToWorldCoords(fsv[1]),ToWorldCoords(endp))
    else: 
        draw.line(dis,fcol,ToWorldCoords(srtp),ToWorldCoords(endp))
        return
    

    
    


while not game_over:
    background.fill(0)
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == all_ui_elements["OXPC"]:polygon_coords[0] = int(event.value)
            if event.ui_element == all_ui_elements["OYPC"]:polygon_coords[1] = int(event.value)
            if event.ui_element == all_ui_elements["OX1LC"]:line_coords[0][0] = int(event.value)
            if event.ui_element == all_ui_elements["OY1LC"]:line_coords[0][1] = int(event.value)
            if event.ui_element == all_ui_elements["OX2LC"]:line_coords[1][0] = int(event.value)
            if event.ui_element == all_ui_elements["OY2LC"]:line_coords[1][1] = int(event.value)
                
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == all_ui_elements["DRAW_POLYGON"]:
                render_pipe[2].clear()
                render_pipe[2].update({"draw.polygon":partial(
                                draw_vect_polygon,background,GREEN,POLYGON,partial(ToWorldCoords,polygon_coords))})
                all_ui_elements["CUT_LINE_1"].show()
                all_ui_elements["CUT_LINE_2"].hide();all_ui_elements["CUT_LINE_3"].hide()    
            if event.ui_element == all_ui_elements["DRAW_RECTANGLE"]:
                render_pipe[2].clear()
                render_pipe[2].update({"draw.rectangle":partial(
                                draw_vect_polygon,background,GREEN,RECTANGLE,partial(ToWorldCoords,polygon_coords))})
                all_ui_elements["CUT_LINE_1"].hide()    
                all_ui_elements["CUT_LINE_2"].show();all_ui_elements["CUT_LINE_3"].show()    
            if event.ui_element == all_ui_elements["DRAW_LINE"]:
                render_pipe[3].clear()
                render_pipe[3].update({"draw.line":partial(
                                draw_vect_line,background,GREEN,partial(ToWorldCoords,line_coords[0]),
                                partial(ToWorldCoords,line_coords[1]))})
            if event.ui_element == all_ui_elements["CUT_LINE_1"]:
                render_pipe[3].clear()
                render_pipe[3].update({"draw.cut_line_1":partial(
                                draw_cut_line_1,background,RED,GREEN,partial(ToWorldCoords,line_coords[0]),
                                partial(ToWorldCoords,line_coords[1]),POLYGON,partial(ToWorldCoords,polygon_coords))})
            if event.ui_element == all_ui_elements["CUT_LINE_2"]:
                render_pipe[3].clear()
                render_pipe[3].update({"draw.cut_line_2":partial(
                                draw_cut_line_2,background,RED,GREEN,partial(ToWorldCoords,line_coords[0]),
                                partial(ToWorldCoords,line_coords[1]),RECTANGLE,partial(ToWorldCoords,polygon_coords)) })
            if event.ui_element == all_ui_elements["CUT_LINE_3"]:
                render_pipe[3].clear()
                render_pipe[3].update({"draw.cut_line_3":partial(
                                draw_cut_line_3,background,RED,GREEN,partial(ToWorldCoords,line_coords[0]),
                                partial(ToWorldCoords,line_coords[1]),RECTANGLE,partial(ToWorldCoords,polygon_coords))})
        manager.process_events(event)
    chain_ui()
    manager.update(time_delta)
    for layer in render_pipe:
        for k in layer:layer[k]()
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    display.update()
pygame.quit()
quit()