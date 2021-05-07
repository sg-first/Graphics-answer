from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import interact

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
    glDepthFunc(GL_LEQUAL)  # 设置深度测试函数（GL_LEQUAL只是选项之一）


def draw():
    global IS_PERSPECTIVE, VIEW
    global EYE, LOOK_AT, EYE_UP
    global SCALE_K
    global WIN_W, WIN_H

    # 清除屏幕及深度缓存
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 设置投影（透视投影）
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if WIN_W > WIN_H:
        if interact.IS_PERSPECTIVE:
            glFrustum(interact.VIEW[0] * WIN_W / WIN_H, interact.VIEW[1] * WIN_W / WIN_H, interact.VIEW[2], interact.VIEW[3],
                      interact.VIEW[4], interact.VIEW[5])
        else:
            glOrtho(interact.VIEW[0] * WIN_W / WIN_H, interact.VIEW[1] * WIN_W / WIN_H, interact.VIEW[2], interact.VIEW[3],
                    interact.VIEW[4], interact.VIEW[5])
    else:
        if interact.IS_PERSPECTIVE:
            glFrustum(interact.VIEW[0], interact.VIEW[1], interact.VIEW[2] * WIN_H / WIN_W, interact.VIEW[3] * WIN_H / WIN_W,
                      interact.VIEW[4], interact.VIEW[5])
        else:
            glOrtho(interact.VIEW[0], interact.VIEW[1], interact.VIEW[2] * WIN_H / WIN_W, interact.VIEW[3] * WIN_H / WIN_W,
                    interact.VIEW[4], interact.VIEW[5])

    # 设置模型视图
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 几何变换
    glScale(interact.SCALE_K[0], interact.SCALE_K[1], interact.SCALE_K[2])

    # 设置视点
    gluLookAt(
        interact.EYE[0], interact.EYE[1], interact.EYE[2],
        interact.LOOK_AT[0], interact.LOOK_AT[1], interact.LOOK_AT[2],
        interact.EYE_UP[0], interact.EYE_UP[1], interact.EYE_UP[2]
    )

    # 设置视口
    glViewport(0, 0, WIN_W, WIN_H)

    # ---------------------------------------------------------------
    glBegin(GL_LINES)  # 开始绘制线段（世界坐标系）

    # 以红色绘制x轴
    glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
    glVertex3f(-0.8, 0.0, 0.0)  # 设置x轴顶点（x轴负方向）
    glVertex3f(0.8, 0.0, 0.0)  # 设置x轴顶点（x轴正方向）

    # 以绿色绘制y轴
    glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
    glVertex3f(0.0, -0.8, 0.0)  # 设置y轴顶点（y轴负方向）
    glVertex3f(0.0, 0.8, 0.0)  # 设置y轴顶点（y轴正方向）

    # 以蓝色绘制z轴
    glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
    glVertex3f(0.0, 0.0, -0.8)  # 设置z轴顶点（z轴负方向）
    glVertex3f(0.0, 0.0, 0.8)  # 设置z轴顶点（z轴正方向）

    glEnd()  # 结束绘制线段

    # ---------------------------------------------------------------
    glBegin(GL_TRIANGLES)  # 开始绘制三角形（z轴负半区）

    glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
    glVertex3f(-0.5, -0.366, -0.5)  # 设置三角形顶点
    glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
    glVertex3f(0.5, -0.366, -0.5)  # 设置三角形顶点
    glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
    glVertex3f(0.0, 0.5, -0.5)  # 设置三角形顶点

    glEnd()  # 结束绘制三角形

    # ---------------------------------------------------------------
    glBegin(GL_TRIANGLES)  # 开始绘制三角形（z轴正半区）

    glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
    glVertex3f(-0.5, 0.5, 0.5)  # 设置三角形顶点
    glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
    glVertex3f(0.5, 0.5, 0.5)  # 设置三角形顶点
    glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
    glVertex3f(0.0, -0.366, 0.5)  # 设置三角形顶点

    glEnd()  # 结束绘制三角形

    # ---------------------------------------------------------------
    glutSwapBuffers()  # 切换缓冲区，以显示绘制内容


def reshape(width, height):
    global WIN_W, WIN_H

    WIN_W, WIN_H = width, height
    glutPostRedisplay()

if __name__ == "__main__":
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    glutInitWindowSize(interact.WIN_W, interact.WIN_H)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('Quidam Of OpenGL')

    init()  # 初始化画布
    glutDisplayFunc(draw)  # 注册回调函数draw()
    glutReshapeFunc(reshape)  # 注册响应窗口改变的函数reshape()
    glutMouseFunc(interact.mouseclick)  # 注册响应鼠标点击的函数mouseclick()
    glutMotionFunc(interact.mousemotion)  # 注册响应鼠标拖拽的函数mousemotion()
    glutKeyboardFunc(interact.keydown)  # 注册键盘输入的函数keydown()

    glutMainLoop()  # 进入glut主循环
