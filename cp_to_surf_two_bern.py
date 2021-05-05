import numpy as np
from scipy.special import comb
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def compute_bernstein_value(order, control_point_index, t):
    return comb(order, control_point_index) * t ** control_point_index * (1.0 - t) ** (order - control_point_index)


if __name__ == "__main__":
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

    # 阶
    assert(x_control_point_matrix.shape == y_control_point_matrix.shape == z_control_point_matrix.shape)
    control_point_u_dimension = x_control_point_matrix.shape[0]
    control_point_v_dimension = y_control_point_matrix.shape[1]
    u_order = control_point_u_dimension - 1
    v_order = control_point_v_dimension - 1

    ###########################################################################
    # Define surface's linear parameter-space distribution
    ###########################################################################
    u_vector = np.linspace(0, 1.0, num=100)
    v_vector = np.linspace(0, 1.0, num=100)

    ###########################################################################
    # Compute surface's Bernstein matrices
    ###########################################################################
    u_bernstein_matrix = np.zeros(shape=(control_point_u_dimension, u_vector.size))
    v_bernstein_matrix = np.zeros(shape=(control_point_v_dimension, v_vector.size))

    for u_control_point_index in range(0, control_point_u_dimension):
        for u_index, u in enumerate(u_vector):
            u_bernstein_matrix[u_control_point_index][u_index] = compute_bernstein_value(u_order, u_control_point_index, u)

    for v_control_point_index in range(0, control_point_v_dimension):
        for v_index, v in enumerate(v_vector):
            v_bernstein_matrix[v_control_point_index][v_index] = compute_bernstein_value(v_order, v_control_point_index, v)

    ###########################################################################
    # Compute surface's real-space distribution
    ###########################################################################
    x_matrix = u_bernstein_matrix.transpose() @ x_control_point_matrix @ v_bernstein_matrix
    y_matrix = u_bernstein_matrix.transpose() @ y_control_point_matrix @ v_bernstein_matrix
    z_matrix = u_bernstein_matrix.transpose() @ z_control_point_matrix @ v_bernstein_matrix

    ###########################################################################
    # Plot surface
    ###########################################################################
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_wireframe(x_matrix, y_matrix, z_matrix)
    plt.title("Torus Patch Defined From Control Points")
    plt.show()
