# https://github.com/ericmdai/CubeSim/blob/master/quat.pq2

import numpy 
from math import *

def normalize(vector,tolerance=0.00001):
#    print("normalize",vector)
    mag2=sum(n*n for n in vector)
    if mag2!=0 and abs(mag2-1.0) > tolerance:
        mag=sqrt(mag2)
        vector=tuple(n/mag for n in vector)
    return vector

def q_mult(p,q):
    p0,p1,p2,p3=p
    q0,q1,q2,q3=q
    r0=p0*q0 - (p1*q1+p2*q2+ p3*q3)    # r0 : p0*q0 -(p.q)
    r1=p1*q0 + p0*q1 + (p2*q3-p3*q2)    # r1,r2,r3 : 
    r2=p2*q0 + p0*q2 + (p3*q1-p1*q3)   # q0*p + p0*q + (p vect q)
    r3=p3*q0 + p0*q3 + (p1*q2-p2*q1)   
    return r0,r1,r2,r3

def q_conjugate(q):
    q0,q1,q2,q3=q
    return (q0,-q1,-q2,-q3)

def q_mult_vector(q1,v1):
    q2 =(0.0,)+v1
    return q_mult(q_mult(q1,q2),q_conjugate(q1))[1:]

def q_axis_to_quaternion(theta,axis):
    axis=normalize(axis)
    q1,q2,q3=axis
    theta=theta*pi/180   # conversion degre/radian
    theta=theta/2.0
    q0=cos(theta)
    q1=q1*sin(theta)
    q2=q2*sin(theta)
    q3=q3*sin(theta)
    return q0,q1,q2,q3

def q_quaternion_to_axis(q):
    q0,axis=q[0],q[1:]
    theta=acos(q0)*2.0
    return theta,normalize(axis)

def q_quaternion_to_matrix(q):
    q0,q1,q2,q3=q
    # y = numpy.array(
    #     [
    #      [1-2*(q2*q2+q3*q3), 2*(q1*q2-q0*q3), 2*(q1*q3+q0*q2), 0],
    #      [2*(q1*q2+q0*q3), 1-2*(q1*q1+q3*q3), 2*(q2*q3-q0*q1), 0],
    #      [2*(q1*q3-q0*q2), 2*(q2*q3+q0*q1), 1-2*(q1*q1+q2*q2), 0],
    #      [0, 0, 0, 1]
    #     ],numpy.float32)
    # need to transpose to OpenGL
    y = numpy.array(
        [
         [1-2*(q2*q2+q3*q3),2*(q1*q2+q0*q3),   2*(q1*q3-q0*q2),  0],
         [2*(q1*q2-q0*q3),  1-2*(q1*q1+q3*q3), 2*(q2*q3+q0*q1),  0],
         [2*(q1*q3+q0*q2),  2*(q2*q3-q0*q1),   1-2*(q1*q1+q2*q2),0],
         [0, 0, 0, 1]
        ],numpy.float32)
    return  y


def matrix_to_quaternion(mat):
    trace=mat[0][0]+mat[1][1]+mat[2][2]
    maxi=max([trace,mat[0][0],mat[1][1],mat[2][2]])
    if maxi==trace :
        q0=sqrt(trace+1.0)/2.0
        q4=4*q0
        q1=(mat[2][1]-mat[1][2])/q4
        q2=(mat[0][2]-mat[2][0])/q4
        q3=(mat[1][0]-mat[0][1])/q4
    elif maxi==mat[0][0] :
        q1=sqrt(2*mat[0][0]-trace+1.0)/2.0
        q4=4*q1
        q0=(mat[2][1]-mat[1][2])/q4
        q2=(mat[1][0]+mat[0][1])/q4
        q3=(mat[0][2]+mat[2][0])/q4
    elif maxi==mat[1][1] :
        q2=sqrt(2*mat[1][1]-trace+1.0)/2.0
        q4=4*q2
        q0=(mat[0][2]-mat[2][0])/q4
        q1=(mat[1][0]+mat[0][1])/q4
        q3=(mat[2][1]+mat[1][2])/q4
    elif maxi==mat[2][2] :
        q3=sqrt(2*mat[2][2]-trace+1.0)/2.0
        q4=4*q3
        q0=(mat[1][0]-mat[0][1])/q4
        q1=(mat[0][2]+mat[2][0])/q4
        q2=(mat[2][1]+mat[1][2])/q4
    return (q0,q1,q2,q3)

