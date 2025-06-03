from sys import argv, exit
from time import sleep
import copy,math

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ("Error: PyOpenGL not installed properly !!")
    sys.exit()

from quaternion import  q_axis_to_quaternion, q_quaternion_to_matrix

from composite import *
from models import *

# Composite 
class TranslationNode(Composite):
    def __init__(self,offset,children=None):
        Composite.__init__(self,children)
        self.offset = offset
    def __repr__(self):
        return "<TranslationNode('{}')>".format(self.offset)
    def draw(self):
        glPushMatrix()
        if callable(self.offset):
            glTranslate(*self.offset())
        else:
            glTranslate(*self.offset)
##        for child in self.children.values():
##            child.draw()
        super(TranslationNode, self).draw()
        glPopMatrix()
    def set_offset(self,offset) :
        self.offset=offset
    def get_offset(self) :
        return self.offset

class RotationNode(Composite):
    def __init__(self,angle,axe,children=None):
        Composite.__init__(self,children)
        self.angle=angle
        self.axe=copy.copy(axe)
    def __repr__(self):
        return "<RotationNode('angle : {}, axe : {} {} {}')>".format(
                    self.angle,
                    self.axe[0],
                    self.axe[1],
                    self.axe[2]
                )
    def draw(self):
        glPushMatrix()
        rx,ry,rz=self.axe
        if callable(self.angle):
            glRotate(self.angle(),rx,ry,rz)
        else:
            glRotate(self.angle,rx,ry,rz)
##        for child in self.children.values():
##            child.draw()
        super(RotationNode, self).draw()
        glPopMatrix()
    def set_angle(self,angle) :
        self.angle=angle
    def get_angle(self) :
        return self.angle
    def set_axe(self,axe) :
        self.axe=copy.copy(axe)
    def get_axe(self) :
        return self.axe

class QuaternionNode(Composite):
    def __init__(self,angle,axe,children=None):
        Composite.__init__(self,children)
        self.angle=angle
        self.axe=copy.copy(axe)
    def __repr__(self):
        q=q_axis_to_quaternion(self.angle,self.axe)
        return "<QuaternionNode(angle:{}, axe:{}, q0:{}, q1:{}, q2:{},q3:{})>".format(
                    self.angle,
                    self.axe,
                    q[0],
                    q[1],
                    q[2],
                    q[3]
                )
    def draw(self):
        glPushMatrix()
        q=q_axis_to_quaternion(self.angle,self.axe)
        mat=q_quaternion_to_matrix(q)
        glMultMatrixf(mat)
##        for child in self.children.values():
##            child.draw()
        super(QuaternionNode, self).draw()
        glPopMatrix()

    def set_axe(self,axe) :
        self.axe=axe
    def get_axe(self) :
        return self.axe
    def set_angle(self,angle) :
        self.angle=angle
    def get_angle(self) :
        return self.angle


class ScaleNode(Composite):
    def __init__(self,factor,children=None):
        Composite.__init__(self,children)
        self.factor = factor
    def __repr__(self):
        return "<ScaleNode('{}')>".format(self.factor)
    def draw(self):
        glPushMatrix()
        if callable(self.factor):
            glScale(*self.factor())
        else:
            glScale(*self.factor)
##        for child in self.children.values():
##            child.draw()
        super(ScaleNode, self).draw()
        glPopMatrix()
    def set_factor(self,factor) :
        self.factor=factor
    def get_factor(self) :
        return self.factor

# Primitives

class Point(Leaf) :
    def __init__(self,point):
        Leaf.__init__(self)
        self.point=copy.copy(point)
    def __repr__(self):
        return "<Point('{} {} {}')>".format(
                    self.point[0],
                    self.point[1],
                    self.point[2])
    def draw():
        glBegin(GL_POINTS)
        x,y,z=self.point
        glVertex(x,y,z)
        glEnd()

    def set_point(self,point) :
        self.point=copy.copy(point)
    def get_point(self) :
        return self.point

class Triangle(Leaf) :
    def __init__(self,p1,p2,p3):
        Leaf.__init__(self)
        self.p1,self.p2,self.p3=p1,p2,p3
    def __repr__(self):
        return "<Triangle('{}, {}, {}')>".format(self.p1,self.p2,self.p3)
    def draw(self):
#         print("Triangle.draw()")
        glBegin(GL_TRIANGLES)
        x1,y1,z1=self.p1.get_point()
        x2,y2,z2=self.p2.get_point()
        x3,y3,z3=self.p3.get_point()
        glVertex(x1,y1,z1)
        glVertex(x2,y2,z2)
        glVertex(x3,y3,z3)
        glEnd()
    def set_points(self,p1,p2,p3) :
        self.p1,self.p2,self.p3=p1,p2,p3
    def get_points(self) :
        return self.p1,self.p2,self.p3

class Quadrilatere(Leaf) :
    def __init__(self,p1,p2,p3,p4):
        Leaf.__init__(self)
        self.p1,self.p2,self.p3,self.p4=p1,p2,p3,p4
    def __repr__(self):
        return "<Quadrilatere('{}, {}, {},{}')>".format(self.p1,self.p2,self.p3,self.p4)
    def draw(self):
#         print("Triangle.draw()")
        glBegin(GL_TRIANGLES)
        x1,y1,z1=self.p1.get_point()
        x2,y2,z2=self.p2.get_point()
        x3,y3,z3=self.p3.get_point()
        glVertex(x1,y1,z1)
        glVertex(x2,y2,z2)
        glVertex(x3,y3,z3)
        glEnd()
    def set_points(self,p1,p2,p3,p4) :
        self.p1,self.p2,self.p3,self.p4=p1,p2,p3,p4
    def get_points(self) :
        return self.p1,self.p2,self.p3,self.p4
    def draw(self):
        glBegin(GL_QUADS)
        x1,y1,z1=self.p1.get_point()
        x2,y2,z2=self.p2.get_point()
        x3,y3,z3=self.p3.get_point()
        x4,y4,z4=self.p4.get_point()
        glVertex(x1,y1,z1)
        glVertex(x2,y2,z2)
        glVertex(x3,y3,z3)
        glVertex(x4,y4,z4)
        glEnd()

class Cube(Leaf) :
    def __init__(self,size):
        Leaf.__init__(self)
        self.size=size
    def __repr__(self):
        return "<Cube({})>".format(self.size)
    def draw(self):
        glutWireCube(self.size)

class Sphere(Leaf) :
    def __init__(self,radius,slices,stacks):
        Leaf.__init__(self)
        self.radius=radius
        self.slices=slices
        self.stacks=stacks
    def __repr__(self):
        return "<Sphere({},{},{})>".format(self.radius,self.slices,self.stacks)
    def draw(self):
        glutWireSphere(self.radius,self.slices,self.stacks)

class Cone(Leaf) :
    def __init__(self,base,height,slices,stacks):
        Leaf.__init__(self)
        self.base=base
        self.height=height
        self.slices=slices
        self.stacks=stacks
    def __repr__(self):
        return "<Sphere({},{},{})>".format(self.base,self.height,self.slices,self.stacks)
    def draw(self):
        glutWireCone(self.base,self.height,self.slices,self.stacks)

class Torus(Leaf) :
    def __init__(self,inner,outer,nsides,rings):
        Leaf.__init__(self)
        self.inner=inner
        self.outer=outer
        self.nsides=nsides
        self.rings=rings
    def __repr__(self):
        return "<Torus({},{},{},{})>".format(self.inner,self.outer,self.nsides,self.rings)
    def draw(self):
        glutWireTorus(self.inner,self.outer,self.nsides,self.rings)

class Teapot(Leaf) :
    def __init__(self,size):
        Leaf.__init__(self)
        self.size=size
    def __repr__(self):
        return "<Teapot({})>".format(self.size)
    def draw(self):
        glutWireTeapot(self.size)

class OCS(Leaf) :
    def __init__(self,size,visible=False):
        Leaf.__init__(self)
        self.size=size
        self.visible=visible
    def __repr__(self):
        return "<OCS({})>".format(self.size)
    def draw(self):
        if self.visible :
            wcs(self.size)
    def set_visible(self,visible):
        self.visible=visible

class Joint(Leaf) :
    # Constructor for the bone class
    def __init__(self,name="joint",radius=1.0) :
        self.name=name
        self.radius=radius
    def draw(self) :
        glPushMatrix()                                 #  bone creation push()
        glColor3f(0.0, 1.0, 0.0)
        sphere(self.radius)
        glPopMatrix()                                  #  bone creation pop()

class Bone(Leaf) :
    def __init__(self,name="bone",dimension=(1.0,1.0,1.0)) :
        self.name=name
        self.base,self.top,self.length=dimension
 
    def draw(self) :
        glPushMatrix()
        glColor3f(1.0, 0.0, 0.0)
        cylinder(self.base,self.top,self.length)
        glTranslatef(0.0,0.0,self.length)
        glColor3f(0.0, 1.0, 0.0)
        sphere(self.base)
        glPopMatrix()                                

    def get_name(self) :
        return self.name
    def get_length(self) :
        return self.length

class Head(Leaf) :
    def __init__(self,name="head",radius=1.0,nose=1.0) :
        self.name=name
        self.radius=radius
        self.nose=nose
 
    def draw(self) :
        glPushMatrix()
        glColor3f(0.0,0.0,1.0)
        sphere(self.radius)
        glTranslatef(0,0,self.radius)                                           # nose positioning
        glColor3f(1.0,0.0,1.0)
        axe(self.nose)
        glTranslatef(self.radius*0.5,self.radius*0.5,-self.radius*0.5)
        sizing=0.1
        glColor3f(0.0,1.0,1.0)                                                  # eyes positioning
        cylinder(self.radius*sizing,self.radius*sizing,self.radius*0.4)
        glTranslatef(-self.radius,0,0)
        cylinder(self.radius*sizing,self.radius*sizing,self.radius*0.4)
        glPopMatrix()                                

    def get_name(self) :
        return self.name
    def get_radius(self) :
        return self.radius
    def get_nose(self) :
        return self.nose
    def set_nose(self,nose) :
        self.nose=nose

class SomethingToDraw(Leaf):
    def __init__(self,func):
        Leaf.__init__(self)
        self.func = func
    def __repr__(self):
        return "<SomethingToDraw()>"
    def draw(self):
        glColor(0,0,0)
        glPushMatrix()
        self.func()
        glPopMatrix()
