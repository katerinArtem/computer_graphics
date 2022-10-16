#Алгоритм  XOR-2 с перегородкой
import sys,os,pygame,pygame_gui,itertools
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


class cell:
    cell_matrix:list[list["cell"]]
    dcol = WHITE
    def __init__(self,model,pos,width,color = dcol):
        self.model = [[p[0]+pos[0],p[1]+pos[1]] for p in model]
        self.color = color
        self.pos = pos
        self.width = width
    def render(self):
        draw.polygon(background,self.color,[ToWorldCoords(p) for p in self.model])
        draw.circle(background,RED,ToWorldCoords([self.pos[0],self.pos[1]]),1)
    def setCell(color,pos):
        if abs(pos[0]+1) < DIS_WIDTH/2 and abs(pos[1]+1) < DIS_HEIGHT/2: 
            cell.cell_matrix[WorldToPix(pos)[0]][WorldToPix(pos)[1]].color = color
        else:print("pixel out of range")
    def render_matrix():
        for l in cell.cell_matrix:
            for c in l:c.render()
    def clear():
        for l in cell.cell_matrix:
            for c in l:c.color = WHITE
    def fill_polygon(col,model,pcntr):
        pcntr = ToScreenCoords(pcntr())
        pol = [WorldToPix([x[0]+pcntr[0],x[1]+pcntr[1]]) for x in model]
        x_avg = round((max(pol,key=lambda k:k[0])[0] + min(pol,key=lambda k:k[0])[0])/2)
        cnt = 0
        lines:list[list] = []
        for p1,p2 in zip(pol,pol[1:]+pol[:1]):
            if cnt < fill_step:
                line:list = []
                A,B = p1,p2
                if A[1] == B[1]:
                    line.append(A)
                    line.append(B)
                    continue
                steep = abs(B[1]-A[1]) > abs(B[0]-A[0])
                x0,x1,y0,y1 = (A[1],B[1],A[0],B[0]) if steep else (A[0],B[0],A[1],B[1])
                dx,dy = abs(x1-x0),abs(y1-y0)
                er,der,y = 0,(dy + 1),y0
                p_old = None
                ix = (1 if x1-x0 >= 0 else -1)
                for x in range(x0,x1+ix,ix):
                    if ((x if steep else y) != (p_old[1] if p_old != None else None)):
                        line.append([y,x] if steep else [x,y])#
                    elif x == x1:
                        line.remove(p_old)
                        line.append([y,x] if steep else [x,y])
                    #line.append([y,x] if steep else [x,y])#
                    er += der
                    p_old = ([y,x] if steep else [x,y])
                    if er >= (dx + 1):
                        y += (1 if y1-y0 >= 0 else -1)
                        er -= (dx + 1)
                    
                cnt +=1
                if cnt != fill_step:
                    lines.append(line)

        all_pnts = []

        if len(lines) != 1:
            for i in range(len(lines)):
                j = i + 1 if i+1 < len(lines) else 0
                line1,line2 = lines[i],lines[j]  
                p_up1 = max([line1[0],line1[-1]],key=lambda k:k[1])
                p_dn1 = min([line1[0],line1[-1]],key=lambda k:k[1])
                p_up2 = max([line2[0],line2[-1]],key=lambda k:k[1])
                p_dn2 = min([line2[0],line2[-1]],key=lambda k:k[1])
                if p_up1 == p_up2:
                    lines[i].remove(p_up1)
                    lines[j].remove(p_up2)
                if p_dn1 == p_dn2:
                    lines[i].remove(p_dn1)
                    lines[j].remove(p_dn2)
                elif p_up1 == p_dn2:lines[i].remove(p_up1)
                elif p_up2 == p_dn1:lines[j].remove(p_up2)   

        for l in lines:all_pnts += l

        gp = [list(g[1]) for g in itertools.groupby(sorted(all_pnts,key=lambda k:k[1]),key=lambda k:k[1])]
        for g in gp:
            for p in g:
                cell.setCell(col,PixToWorld(p))
                s = p[0] if x_avg - p[0] >= 0 else x_avg
                e = p[0] if x_avg - p[0] < 0 else x_avg
                for x in range(s,e):
                    try:
                        if cell.cell_matrix[x][p[1]].color == cell.dcol:
                            cell.cell_matrix[x][p[1]].color = col
                        else:
                            cell.cell_matrix[x][p[1]].color = cell.dcol
                    except:pass
                    
                                
            


            
def cellMatrix() -> list:
    matrix = []
    for x in range(-int(DIS_WIDTH/2),int(DIS_WIDTH/2),PIX_SIZE):
        line = []
        for y in range(-int(DIS_HEIGHT/2),int(DIS_HEIGHT/2),PIX_SIZE):
            line.append(cell([[p[0]+1,p[1]+1] for p in CELL],[x,y],PIX_SIZE,WHITE))
        matrix.append(line)
    return matrix
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
        "DRAW_POLYGON":set_button('нарисовать полигон',300,0),
        "OXPC":set_slider(300,25),"OXPCTB":set_textbox(50,25),
        "OYPC":set_slider(300,50),"OYPCTB":set_textbox(50,50),
        "FILL_POLYGON":set_button('заполнить полигон',300,75),
    }
    ui["FILL_POLYGON"].hide()
    return ui

def chain_ui():
    def tb_n_sl(sl,tb,v):
        all_ui_elements[sl].set_current_value(float(v))
        all_ui_elements[tb].set_text(str(v))

    tb_n_sl("OXPC","OXPCTB",polygon_coords[0])
    tb_n_sl("OYPC","OYPCTB",polygon_coords[1])


def draw_vect_polygon(dis,col,model,cntr):
    draw.polygon(dis,col,[[x[0]+cntr()[0],-x[1]+cntr()[1]] for x in model],width=2)
    #draw midle line
    cntr = ToScreenCoords(cntr())
    pol = [WorldToPix([x[0]+cntr[0],x[1]+cntr[1]]) for x in model]
    y_min = min(pol,key=lambda k:k[1])[1]
    y_max = max(pol,key=lambda k:k[1])[1]
    x_avg = round((max(pol,key=lambda k:k[0])[0] + min(pol,key=lambda k:k[0])[0])/2)
    A = PixToWorld([x_avg,y_min])
    B = PixToWorld([x_avg,y_max])
    draw.line(dis,YELLOW,ToWorldCoords(A),ToWorldCoords(B))


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
polygon_coords = [0,0]
fill_step = 0

render_pipe.append({})#0 layer
render_pipe.append({})#1 layer
render_pipe.append({})#2 layer
render_pipe.append({})#3 layer
render_pipe.append({})#4 layer

render_pipe[0].update({"cell.render_matrix":partial(cell.render_matrix)})
render_pipe[0].update({"cell.clear":partial(cell.clear)})

render_pipe[1].update({"decart":partial(decart)})



while not game_over:
    background.fill(0)
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == all_ui_elements["OXPC"]:polygon_coords[0] = int(event.value)
            if event.ui_element == all_ui_elements["OYPC"]:polygon_coords[1] = int(event.value)

                
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == all_ui_elements["DRAW_POLYGON"]:
                render_pipe[2].clear()
                render_pipe[2].update({"draw.polygon":partial(
                                draw_vect_polygon,background,RED,POLYGON,partial(ToWorldCoords,polygon_coords))})
                all_ui_elements["FILL_POLYGON"].show()  
            if event.ui_element == all_ui_elements["FILL_POLYGON"]:
                fill_step += 1
                if fill_step-1 > POLYGON.__len__():fill_step = 0
                render_pipe[3].clear()
                render_pipe[3].update({"cell.fill_polygon":partial(
                                cell.fill_polygon,PINK,POLYGON,partial(ToWorldCoords,polygon_coords))})
                
            
        
                
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

