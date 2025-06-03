# -*- coding: utf-8 -*-
from sys import argv, exit
from time import sleep
from math import pi,sin,cos
from composite  import *

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    import math
except:
    print("Error: PyOpenGL not installed properly !!")
    sys.exit()

def sphere(radius,longitude=20,latitude=10) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluSphere(params,radius,longitude,latitude)
  gluDeleteQuadric(params)

def cylinder(base,top,height,slices=20,stacks=10) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluCylinder(params,base,top,height,slices,stacks)
  gluDeleteQuadric(params)
def disk(inner,outer,slices=10,loops=5) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluDisk(params,inner,outer,slices,loops)
  gluDeleteQuadric(params)

def stick(base,top,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  glColor3f(1,0,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  glColor3f(0,1,0)
  cylinder(base,top,height,slices,stacks)
  glPushMatrix()
  glTranslatef(0,0,height)
  glColor3f(1,0,0)
  disk(0,top,slices,stacks)
  glPopMatrix()

def cone(base,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  cylinder(base,0,height,slices,stacks)

def torus(inner,outer,sides=10,rings=5) :
  glutSolidTorus(inner,outer,sides,rings)

def floor(size,position=[0.0,0.0,0.0],tiles=10) :
    tile_size=size/tiles
    glPushMatrix()
    glTranslatef(position[0],position[1],position[2])
    for i in range(10+1) :
        for j in range(10+1) :
            glPushMatrix()
        #        glTranslatef(-size/2.0+tile_size*i,-1.0,-size/2.0+tile_size*j)
            glTranslatef(-size/2.0+tile_size*i,0.0,-size/2.0+tile_size*j)
            if (i+j)%2 == 0 :
                glColor3f(1.0,1.0,1.0)
                glRotatef(-90,1,0,0)
                glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
            else :
                glColor3f(0.0,0.0,0.0)
                glRotatef(90,1,0,0)
                glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
            glPopMatrix()
    glPopMatrix()

def axe(size) :
    cylinder(0.08*size,0.08*size,size)
    glPushMatrix()
    glTranslatef(0,0,size)
    cylinder(0.1*size,0,0.25*size)
    glPopMatrix()

def wcs(size) :
    glColor3ub(0,0,255)        # Oz (blue)
    axe(size)
    glPushMatrix()
    glRotatef(-90.0, 1, 0, 0)
    glColor3ub(0,255,0)        # Oy (green)
    axe(size)
    glPopMatrix()
    glPushMatrix()
    glRotatef(90.0, 0, 1, 0)
    glColor3ub(255,0,0)        # Ox (red)
    axe(size)
    glPopMatrix()
