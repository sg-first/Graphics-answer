import taichi as ti
import numpy as np
import stack
import math

ti.init(arch=ti.gpu) # Try to run on GPU
size=1000

# 名字的线
startPos=[150,80]
allLine=[]

allLine.append([[160,116],[266,107]])
allLine.append([[266,107],[208,202]])
allLine.append([[208,202],[280,182]])
allLine.append([[280,182],[213,343]])
allLine.append([[180,260],[449,323]])
allLine.append([[393,94],[307,129]])
allLine.append([[362,102],[367,234]])
allLine.append([[302,176],[407,156]])
allLine.append([[289,242],[436,238]])

allLine=np.array(allLine)
startPos=np.array(startPos)
allLine=allLine-startPos

img = np.zeros((size, size))
boundary_color=0.9

def bresenham(x0, y0, x1, y1):
    if x0>x1:
        x0,y0,x1,y1=x1,y1,x0,y0

    dx=x1-x0
    dy=y1-y0
    k=dy/dx
    step=0.1

    y=y0
    x=x0
    allPos = []

    if dx>=dy:
        while x<=x1:
            rx=int(x)
            ry=size-int(y+0.5)
            img[rx,ry]=boundary_color # y+0.5相当于四舍五入，size-规范化坐标
            allPos.append((rx,ry))
            y += k * step
            x += step
    else:
        k=1/k
        while y <= y1:
            rx = int(x + 0.5)
            ry = size - int(y)
            img[rx, ry] = boundary_color  # y+0.5相当于四舍五入，size-规范化坐标
            allPos.append((rx, ry))
            y += step
            x += k*step
    return allPos

fill_Color=0.5
def fill(l11,l11d,l22,l22d):
    allX=[l11[0],l11d[0],l22[0],l22d[0]]
    allY=[size-l11[1],size-l11d[1],size-l22[1],size-l22d[1]]

    seed=int((max(allX)+min(allX))/2),int((max(allY)+min(allY))/2)

    s=stack.Stack()
    s.push(seed)
    upOver=False
    while s.size()!=0:
        x,y=s.pop()
        savex=x
        while img[x,y]!=boundary_color:
            img[x,y]=fill_Color
            if img[x,y+1]==boundary_color or img[x,y-1]==boundary_color:
                break
            x += 1
        xright=x-1
        x=savex-1
        while img[x,y]!=boundary_color:
            img[x,y]=fill_Color
            if img[x,y+1]==boundary_color or img[x,y-1]==boundary_color:
                break
            x -= 1
        xleft=x+1
        x = int((xleft + xright) / 2)

        if not upOver:
            y += 1  # 看下一行
            if img[x, y] != boundary_color and y < max(allY):
                s.push((x, y))
            else: # 下面的都处理完了，可以处理上面的
                upOver=True
                s.push(seed)
        else:
             y -= 1  # 看上一行
             if img[x, y] != boundary_color and y > min(allY):
                 s.push((x, y))

bou_Color=1
def setColor(allPos):
    for x,y in allPos:
        img[x,y]=bou_Color

def drawName(x,y,x1,y1,allLine):
    d=np.array([x,y])
    d1=np.array([x1,y1])
    for l1,l2 in allLine:
        l11=l1+d
        l22=l2+d
        allPos=bresenham(l11[0], l11[1], l22[0], l22[1])
        l11d=l11+d1
        l22d=l22+d1
        allPos+=bresenham(l11d[0], l11d[1], l22d[0], l22d[1])
        allPos+=bresenham(l11[0], l11[1], l11d[0], l11d[1])
        allPos+=bresenham(l22[0], l22[1], l22d[0], l22d[1])
        fill(l11,l11d,l22,l22d)
        setColor(allPos)

dire=True
def colorChange():
    global fill_Color, dire
    if dire:
        fill_Color-=0.1
    else:
        fill_Color+=0.1
    if fill_Color==0.9:
        if dire:
            fill_Color=0.8
        else:
            fill_Color=1
    elif fill_Color<=0:
        dire=False
    elif fill_Color>=1:
        dire=True

def trans(allLine, transMat):
    newLine=allLine.copy()
    for i in newLine:
        i[0] = np.dot(i[0], transMat)
        i[1] = np.dot(i[1], transMat)
    return newLine

shear=np.array([[1,0.3],[0.2,1]])
scale=np.array([[1.5,0],[0,2]])
rotate=np.array([[math.cos(30),-math.sin(30)],[math.sin(30),math.cos(30)]])
shearPos=trans(allLine,shear)
scalePos=trans(allLine,scale)
rotatePos=trans(allLine,rotate)

gui = ti.GUI("Taichi", res=size)
frame=30
while True:
    drawName(0, 0, 20, 20, shearPos)
    drawName(250, 0, 20, 20, scalePos)
    drawName(250, 250, 20, 20, rotatePos)
    '''
    frame-=1
    if frame==0:
        frame=1
        colorChange()
    '''
    gui.set_image(img)
    gui.show() # Change to gui.show(f'{frame:06d}.png') to write images to disk