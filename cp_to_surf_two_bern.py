import numpy as np
from scipy.special import comb
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import interact

def compute_bernstein_value(order, control_point_index, t):
    return comb(order, control_point_index) * t ** control_point_index * (1.0 - t) ** (order - control_point_index)

# 控制点
x_control_point_matrix = np.array([
    [2.99846590, 3.00844079, 2.47012264, 1.61960384],
    [3.00179002, 3.01177595, 2.47286102, 1.62139934],
    [2.82239653, 2.83178568, 2.32507747, 1.52450099],
    [2.53896277, 2.54740903, 2.09158602, 1.37140590]
])

y_control_point_matrix = np.array([
    [-0.00056355, 1.00378404, 1.98916880, 2.52342656],
    [-0.00056417, 1.00489684, 1.99137400, 2.52622403],
    [-0.00053046, 0.94484202, 1.87236516, 2.37525140],
    [-0.00047719, 0.84995807, 1.68433648, 2.13672133]
])

z_control_point_matrix = np.array([
    [-0.00018787, -0.00018787, -0.00018787, -0.00018787],
    [ 0.33463746,  0.33463746,  0.33463746,  0.33463746],
    [ 0.66314105,  0.66314105,  0.66314105,  0.66314105],
    [ 0.84124974,  0.84124974,  0.84124974,  0.84124974]
])

def solve(x_control_point_matrix, y_control_point_matrix, z_control_point_matrix,step=10):
    # 阶
    assert(x_control_point_matrix.shape == y_control_point_matrix.shape == z_control_point_matrix.shape)
    control_point_u_dimension = x_control_point_matrix.shape[0]
    control_point_v_dimension = y_control_point_matrix.shape[1]
    u_order = control_point_u_dimension - 1
    v_order = control_point_v_dimension - 1

    # uv空间参数
    u_vector = np.linspace(0, 1.0, num=step)
    v_vector = np.linspace(0, 1.0, num=step)

    # 计算matrices
    u_bernstein_matrix = np.zeros(shape=(control_point_u_dimension, u_vector.size))
    v_bernstein_matrix = np.zeros(shape=(control_point_v_dimension, v_vector.size))

    for u_control_point_index in range(0, control_point_u_dimension):
        for u_index, u in enumerate(u_vector):
            u_bernstein_matrix[u_control_point_index][u_index] = compute_bernstein_value(u_order, u_control_point_index, u)

    for v_control_point_index in range(0, control_point_v_dimension):
        for v_index, v in enumerate(v_vector):
            v_bernstein_matrix[v_control_point_index][v_index] = compute_bernstein_value(v_order, v_control_point_index, v)

    # 计算曲面真实坐标
    x_matrix = u_bernstein_matrix.transpose() @ x_control_point_matrix @ v_bernstein_matrix
    y_matrix = u_bernstein_matrix.transpose() @ y_control_point_matrix @ v_bernstein_matrix
    z_matrix = u_bernstein_matrix.transpose() @ z_control_point_matrix @ v_bernstein_matrix

    return x_matrix, y_matrix, z_matrix

x_matrix, y_matrix, z_matrix = solve(x_control_point_matrix, y_control_point_matrix, z_control_point_matrix)

x_matrix-=x_matrix.mean()
y_matrix-=y_matrix.mean()
z_matrix-=z_matrix.mean()

# 绘制
def draw():
    interact.drawInit()

    a=0.1
    b=0.1
    glBegin(GL_QUADS)
    for i in range(9):
        for j in range(9):
            glColor3f(a, b, 0)
            glVertex3f(x_matrix[i,j], y_matrix[i,j], z_matrix[i,j])
            glVertex3f(x_matrix[i+1,j], y_matrix[i+1,j], z_matrix[i+1,j])
            glVertex3f(x_matrix[i+1,j+1], y_matrix[i+1,j+1], z_matrix[i+1,j+1])
            glVertex3f(x_matrix[i,j+1], y_matrix[i,j+1], z_matrix[i,j+1])
            b+=0.1
        a+=0.1
    glEnd()

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