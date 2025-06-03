# -*- coding: utf-8 -*-
from sys import argv, exit
from time import sleep
from math import pi, sin, cos
from composite import *
from models import *
from scene_graph import *

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    import math
except:
    print("Error: PyOpenGL not installed properly!!")
    sys.exit()

class Humanoid(Composite):
    def __init__(self, name="pinocchio", size=1.0, position=[0.0, 0.0, 0.0], orientation=[0.0, 0, 1, 0]):
        Composite.__init__(self)
        self.name = name
        self.size = size
        self.position, self.orientation = position, orientation
        self.quaternion = True

        node_position = TranslationNode(self.position)
        self.add(self.name + "_position", node_position)
        angle = self.orientation[0]
        axes = self.orientation[1], self.orientation[2], self.orientation[3]
        node = RotationNode(angle, axes)
        node_position.add(self.name + "_orientation", node)

        self.pelvis(node)
        ocs = OCS(size)
        self.lower_body(node)

        names = []
        self.get_children_names(names)
        print(names)

    def pelvis(self, node):
        joint = Joint(radius=self.size * 0.3)
        node.add(self.name + "_Pelvis", joint)
        return node

    def skeleton_joint(self, node, name, position=(0.0, 0.0, 0.0), orientation=(0.0, 0, 1, 0), scaling=1.0):
        dim_x = 0.2 * self.size * scaling
        dim_y = 0.1 * self.size * scaling
        dim_z = self.size * scaling
        dimension = dim_x, dim_y, dim_z
        theta = orientation[0]
        ox, oy, oz = orientation[1], orientation[2], orientation[3]

        node_position = TranslationNode(position)
        node.add(name + "_position", node_position)

        if self.quaternion:
            node = QuaternionNode(theta, (ox, oy, oz))
        else:
            node = RotationNode(theta, (ox, oy, oz))
        
        node_position.add(name + "_orientation", node)
        bone = Bone(name, dimension)
        node.add(name, bone)
        return node

    def lower_body(self, node):
        self.hip_leg_knee(node)
        self.hip_leg_knee(node, side="Left")

    def hip_leg_knee(self, node, side="Right"):
        if side == "Right":
            hip_position = (self.size * 0.05, -self.size * 0.06, 0.0)
        else:
            hip_position = (-self.size * 0.05, -self.size * 0.06, 0.0)

        orientation = (0.0, 1, 0, 0)
        hip_name = self.name + "_" + side + "Hip"
        hip_node = self.skeleton_joint(node, hip_name, hip_position, orientation, scaling=0.8)

        lower_leg_name = self.name + "_" + side + "LowerLeg"
        lower_leg_position = (0.0, -self.size * 0.06, 0.0)
        self.skeleton_joint(hip_node, lower_leg_name, lower_leg_position, orientation, scaling=0.5)

    def chest(self, node, resizing=0.75):
        pass

    def upper_body(self, node):
        self.collar_choulder_arm(node)
        self.collar_choulder_arm(node, side="Left")

    def collar_choulder_arm(self, node, side="Right", resizing=0.75):
        pass

    def head(self, node):
        pass

    def get_name(self):
        return self.name


def display():
    """Glut display function."""
    global model, size, wcs_on, ocs_on
    glClearColor(0.5, 0.5, 0.5, 0.5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(3, 4, 2, 0, 0, 0, 0, 1, 0)
    glPushMatrix()
    glTranslatef(0, -2 * size, 0)
    if wcs_on:
        wcs(size)
        floor(10 * size)
    glPopMatrix()
    
"""
    node = model.get_child(model.get_name() + "_ocs")
    if node:
        node.set_visible(ocs_on)
    model.draw()"""



def reshape(w, h):
    foc, ratio = 60.0, w * 1.0 / h
    near, far = 0.1, 100.0
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(foc, ratio, near, far)


def on_normal_key_action(key, x, y):
    global model, size, wcs_on, ocs_on, right_on
    name = model.get_name()

    # Handle key actions
    # This section includes the control logic for the humanoid skeleton and other functionalities.

    glutPostRedisplay()


def on_special_key_action(key, x, y):
    global model
    if key == GLUT_KEY_DOWN:
        orientation = model.get_child(model.get_name() + "_orientation").get_angle()
        node = model.get_child(model.get_name() + "_position")
        x, y, z = node.get_offset()
        x -= 0.1 * size * cos(orientation * pi / 180.0)
        z += 0.1 * size * sin(orientation * pi / 180.0)
        node.set_offset((x, y, z))
    elif key == GLUT_KEY_UP:
        orientation = model.get_child(model.get_name() + "_orientation").get_angle()
        node = model.get_child(model.get_name() + "_position")
        x, y, z = node.get_offset()
        x += 0.1 * size * cos(orientation * pi / 180.0)
        z -= 0.1 * size * sin(orientation * pi / 180.0)
        node.set_offset((x, y, z))
    elif key == GLUT_KEY_LEFT:
        node = model.get_child(model.get_name() + "_orientation")
        node.set_angle(node.get_angle() + 1)
    elif key == GLUT_KEY_RIGHT:
        node = model.get_child(model.get_name() + "_orientation")
        node.set_angle(node.get_angle() - 1)
    else:
        pass
    glutPostRedisplay()


if __name__ == "__main__":
    global size, wcs_on, ocs_on, right_on
    size = 1.0
    wcs_on, ocs_on, right_on = False, False, True
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    glutInitWindowSize(1200, 1000)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(sys.argv[0])
    model = Humanoid(size=size)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(on_normal_key_action)
    glutSpecialFunc(on_special_key_action)
    glutMainLoop()
