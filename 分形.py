import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import interact
import random
import copy

quadric=gluNewQuadric()

class cylinder:
    def __init__(self,z,angle,width,height,color):
        self.z=z
        self.angle=angle
        self.width=width
        self.height=height
        self.color=color
        self.subCylinder=[]

    def draw(self):
        glColor3f(self.color[0], self.color[1], self.color[2])
        glTranslatef(0.0, 0, self.z)
        glRotatef(self.angle, 1, 0, 0)
        print(self.z,self.angle)
        gluCylinder(quadric, self.width, self.width, self.height, 30, 1)
        for i in self.subCylinder:
            i.draw()
        glRotatef(-self.angle, 1, 0, 0)
        glTranslatef(0.0, 0, -self.z)

def randColor(color):
    step=0.3
    sub=random.randint(0,2)
    c=random.randint(0,1)
    if c==0:
        color[sub]+=step
    else:
        color[sub]-=step

    if color[sub]>1:
        color[sub]-=step
        return randColor(color)
    elif color[sub]<0:
        color[sub]+=step
        return randColor(color)
    else:
        return color

root=cylinder(0,0,0.75,5,[1,1,0])
def recuTree(width,height,color,parent=None,layer=0):
    if layer==3:
        return
    newColor=randColor(copy.copy(color))
    if layer!=0:
        detZ = height*(random.randint(0, 5)/10)
        detAngle = 180+random.randint(-60, 60)
        detWidth = random.randint(4, 8)/10
        detHeight = random.randint(4, 8)/10
        width*=detWidth
        height*=detHeight
        c = cylinder(detZ, detAngle, width, height, newColor)
        parent.subCylinder.append(c)
        parent = c
    # 递归
    num=random.randint(3, 10)
    for _ in range(2):
        recuTree(width,height,newColor,parent,layer+1)

recuTree(0.7,5,[1,1,0],root)

def draw():
    interact.drawInit()
    # glBegin(GL_QUADS)
    glRotatef(90, 1, 0, 0)
    '''
    gluCylinder(quadric, 0.5, 0.5, 3, 30, 1)
    glTranslatef(0.0, 0, 2.5)
    glRotatef(180-60, 1, 0, 0)
    gluCylinder(quadric, 0.3, 0.3, 2, 30, 1)
    '''
    root.draw()
    # glEnd()
    glutSwapBuffers()  # 切换缓冲区，以显示绘制内容


if __name__ == "__main__":
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    glutInitWindowSize(interact.WIN_W, interact.WIN_H)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('Quidam Of OpenGL')

    interact.init()  # 初始化画布
    glutDisplayFunc(draw)  # 注册回调函数draw()
    glutReshapeFunc(interact.reshape)  # 注册响应窗口改变的函数reshape()
    glutMouseFunc(interact.mouseclick)  # 注册响应鼠标点击的函数mouseclick()
    glutMotionFunc(interact.mousemotion)  # 注册响应鼠标拖拽的函数mousemotion()
    glutKeyboardFunc(interact.keydown)  # 注册键盘输入的函数keydown()

    glutMainLoop()  # 进入glut主循环