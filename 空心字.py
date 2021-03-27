import taichi as ti
import numpy as np

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

def DDA(x0,y0,x1,y1):
    if x0>x1:
        x0,y0,x1,y1=x1,y1,x0,y0

    step=0.01

    dx=x1-x0
    dy=y1-y0
    k=dy/dx
    y=y0

    x=x0
    while x<=x1:
        img[int(x),size-int(y+0.5)]=1 # y+0.5相当于四舍五入，size-规范化坐标
        y+=k*step
        x+=step

def drawName(x,y):
    d=np.array([x,y])
    for l1,l2 in allLine:
        l11=l1+d
        l22=l2+d
        DDA(l11[0],l11[1],l22[0],l22[1])

def draw():
    drawName(20, 70)
    drawName(20, 100)

gui = ti.GUI("Taichi", res=size)
for frame in range(20000):
    draw()
    gui.set_image(img)
    gui.show() # Change to gui.show(f'{frame:06d}.png') to write images to disk