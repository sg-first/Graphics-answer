import taichi as ti
import numpy as np
import stack

ti.init(arch=ti.gpu) # Try to run on GPU
size=640

# 名字的线
startPos=[160,116]
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

'''
num=len(allLine) # 一共多少根线，就是矩阵有多少行
line1=ti.Matrix(allLine[:,0,:])
line2=ti.Matrix(allLine[:,1,:])
'''

img = np.zeros((size, size))
boundary_color=0.9

def DDA(x0,y0,x1,y1):
    if x0>x1:
        x0,y0,x1,y1=x1,y1,x0,y0

    step=0.04

    dx=x1-x0
    dy=y1-y0
    k=dy/dx
    y=y0

    x=x0
    allPos=[]
    while x<=x1:
        rx=int(x)
        ry=size-int(y+0.5)
        img[rx,ry]=boundary_color # y+0.5相当于四舍五入，size-规范化坐标
        allPos.append((rx,ry))
        y+=k*step
        x+=step
    return allPos


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
            img[x,y]=0.5
            x+=1
            if img[x,y+1]==boundary_color or img[x,y-1]==boundary_color:
                break
        xright=x-1
        x=savex-1
        while img[x,y]!=boundary_color:
            img[x,y]=0.5
            x-=1
            if img[x,y+1]==boundary_color or img[x,y-1]==boundary_color:
                break
        xleft=x+1

        if not upOver:
            y += 1  # 看下一行
            x = int((xleft + xright) / 2)
            if img[x, y] != boundary_color and y < max(allY):
                s.push((x, y))
            else: # 下面的都处理完了，可以处理上面的
                upOver=True
                s.push(seed)
        else:
             y -= 1  # 看上一行
             x = int((xleft + xright) / 2)
             if img[x, y] != boundary_color and y > min(allY):
                 s.push((x, y))

def setColor(allPos):
    for x,y in allPos:
        img[x,y]=1

def drawName(x,y,x1,y1):
    d=np.array([x,y])
    d1=np.array([x1,y1])
    aa=0
    for l1,l2 in allLine:
        l11=l1+d
        l22=l2+d
        allPos=DDA(l11[0],l11[1],l22[0],l22[1])
        l11d=l1+d1
        l22d=l2+d1
        allPos+=DDA(l11d[0],l11d[1],l22d[0],l22d[1])
        allPos+=DDA(l11[0],l11[1],l11d[0],l11d[1])
        allPos+=DDA(l22[0],l22[1],l22d[0],l22d[1])
        fill(l11,l11d,l22,l22d)
        setColor(allPos)

def draw():
    drawName(20, 70, 50, 100)

gui = ti.GUI("Taichi", res=size)
for frame in range(20000):
    draw()
    gui.set_image(img)
    gui.show() # Change to gui.show(f'{frame:06d}.png') to write images to disk