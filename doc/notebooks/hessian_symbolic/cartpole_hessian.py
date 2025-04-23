# cartpole_hessian.py
# dew.ninja  April 22, 25
# compute Hessian terms of cartpole dynamics + RK4
# using SymPy, to be used in DDP example.

import numpy as np 
from sympy import symbols,sin,cos,Array,diff,simplify,lambdify

h = 0.05  # time step
def cartpole(x, u):

    c = np.cos(x[1])  # cos(theta)
    s = np.sin(x[1])  # sin(theta)

    # parameters. Changed to match RobotZoo's cartpole
    m_c = 1.0  # cart mass
    m_p = 0.2 # pendulum mass
    l = 0.5  # pole length
    g = 9.81  # gravity

    f1 = x[2]  # x_dot is the 3rd element of state vector
    f2 = x[3]  # theta_dot is the 4th element of state vector
    f3 = (1/(m_c + m_p*s**2))*(u + m_p*s*(l*x[3]**2+g*c))   
    f4 = (1/(l*(m_c + m_p*s**2)))*(-u*c - m_p*l*x[3]**2*c*s - (m_c+m_p)*g*s)  
    y = np.array([f1, f2, f3, f4]).reshape(4,1)
    return y


x1,x2,x3,x4,u = symbols("x1,x2,x3,x4,u")

# create symbolic model of cartpole 
# with parameters conforming to robotzoo's
def create_cartpole_sym():
    m_c = 1.0  # cart mass
    m_p = 0.2 # pendulum mass
    l = 0.5  # pole length
    g = 9.81  # gravity
    s2 = sin(x2)
    c2 = cos(x2)
    f1 = x3
    f2 = x4
    f3 = (1/(m_c + m_p*s2**2))*(u + m_p*s2*(l*x4**2+g*c2))
    f4 = (1/(l*(m_c + m_p*s2**2)))*(-u*c2 - m_p*l*x4**2*c2*s2 - (m_c+m_p)*g*s2)
    cartpole_sym = Array([[f1],[f2],[f3],[f4]])    
    return cartpole_sym

cartpole_sym = create_cartpole_sym()

# elements of Hessian
d2f1_x1sq = diff(cartpole_sym[0],x1,x1)
d2f1_x3sq = diff(cartpole_sym[0],x3,x3)
d2f1_x4sq = diff(cartpole_sym[0],x4,x4)
d2f1_x1x2 = diff(cartpole_sym[0],x1,x2)
d2f1_x1x3 = diff(cartpole_sym[0],x1,x3)
d2f1_x1x4 = diff(cartpole_sym[0],x1,x4)
d2f1_x2sq = diff(cartpole_sym[0],x2,x2)
d2f1_x2x3 = diff(cartpole_sym[0],x2,x3)
d2f1_x3x4 = diff(cartpole_sym[0],x3,x4)
d2f1_x2x4 = diff(cartpole_sym[0],x2,x4)

d2f2_x1sq = diff(cartpole_sym[1],x1,x1)
d2f2_x2x1 = diff(cartpole_sym[1],x2,x1)
d2f2_x2sq = diff(cartpole_sym[1],x2,x2)
d2f2_x3sq = diff(cartpole_sym[1],x3,x3)
d2f2_x4sq = diff(cartpole_sym[1],x4,x4)
d2f2_x2x3 = diff(cartpole_sym[1],x2,x3)
d2f2_x2x4 = diff(cartpole_sym[1],x2,x4)
d2f2_x1x3 = diff(cartpole_sym[1],x1,x3)
d2f2_x1x4 = diff(cartpole_sym[1],x1,x4)
d2f2_x3x4 = diff(cartpole_sym[1],x3,x4)

d2f3_x3x1 = diff(cartpole_sym[2],x3,x1)
d2f3_x3x2 = diff(cartpole_sym[2],x3,x2)
d2f3_x3sq = diff(cartpole_sym[2],x3,x3)
d2f3_x3x4 = diff(cartpole_sym[2],x3,x4)
d2f3_x1sq = diff(cartpole_sym[2],x1,x1)
d2f3_x2sq = diff(cartpole_sym[2],x2,x2)
d2f3_x4sq = diff(cartpole_sym[2],x4,x4)
d2f3_x1x2 = diff(cartpole_sym[2],x1,x2)
d2f3_x1x4 = diff(cartpole_sym[2],x1,x4)
d2f3_x2x4 = diff(cartpole_sym[2],x2,x4)

d2f4_x4x1 = diff(cartpole_sym[3],x4,x1)
d2f4_x4x2 = diff(cartpole_sym[3],x4,x2)
d2f4_x4x3 = diff(cartpole_sym[3],x4,x3)
d2f4_x4sq = diff(cartpole_sym[3],x4,x4)
d2f4_x2sq = diff(cartpole_sym[3],x2,x2)
d2f4_x1sq = diff(cartpole_sym[3],x1,x1)
d2f4_x3sq = diff(cartpole_sym[3],x3,x3)
d2f4_x1x2 = diff(cartpole_sym[3],x1,x2)
d2f4_x1x3 = diff(cartpole_sym[3],x1,x3)
d2f4_x2x3 = diff(cartpole_sym[3],x2,x3)    

# create symbolic Ax array
def create_Ax_sym():
    Ax_sym = Array([
        [d2f1_x1sq, d2f1_x1x2, d2f1_x1x3, d2f1_x1x4],
        [d2f2_x1sq, d2f2_x2x1, d2f2_x1x3, d2f2_x1x4],
        [d2f3_x1sq, d2f3_x1x2, d2f3_x3x1, d2f3_x1x4],
        [d2f4_x1sq, d2f4_x1x2, d2f4_x1x3, d2f4_x4x1],

        [d2f1_x1x2, d2f1_x2sq, d2f1_x2x3, d2f1_x2x4],
        [d2f2_x2x1, d2f2_x2sq, d2f2_x2x3, d2f2_x2x4],
        [d2f3_x1x2, simplify(d2f3_x2sq), d2f3_x3x2, simplify(d2f3_x2x4)],
        [d2f4_x1x2, simplify(d2f4_x2sq), d2f4_x2x3, simplify(d2f4_x4x2)],

        [d2f1_x1x3, d2f1_x2x3, d2f1_x3sq, d2f1_x3x4],
        [d2f2_x1x3, d2f2_x2x3, d2f2_x3sq, d2f2_x3x4],
        [d2f3_x3x1, d2f3_x3x2, d2f3_x3sq, d2f3_x3x4],
        [d2f4_x1x3, d2f4_x2x3, d2f4_x3sq, d2f4_x4x3],
        
        [d2f1_x1x4, d2f1_x2x4, d2f1_x3x4, d2f1_x4sq],
        [d2f2_x1x4, d2f2_x2x4, d2f2_x3x4, d2f2_x4sq],
        [d2f3_x1x4, simplify(d2f3_x2x4), d2f3_x3x4, simplify(d2f3_x4sq)],
        [d2f4_x4x1, simplify(d2f4_x4x2), d2f4_x4x3, simplify(d2f4_x4sq)]
    ])[:,:,0]    
    return Ax_sym

# compute each element in C.16 - C.19.Some are equal.
d2f1_x1u = diff(cartpole_sym[0],x1,u)
d2f1_x2u = diff(cartpole_sym[0],x2,u)
d2f1_x3u = diff(cartpole_sym[0],x3,u)
d2f1_x4u = diff(cartpole_sym[0],x4,u)

d2f2_x1u = diff(cartpole_sym[1],x1,u)
d2f2_x2u = diff(cartpole_sym[1],x2,u)
d2f2_x3u = diff(cartpole_sym[1],x3,u)
d2f2_x4u = diff(cartpole_sym[1],x4,u)

d2f3_x1u = diff(cartpole_sym[2],x1,u)
d2f3_x2u = diff(cartpole_sym[2],x2,u)
d2f3_x3u = diff(cartpole_sym[2],x3,u)
d2f3_x4u = diff(cartpole_sym[2],x4,u)

d2f4_x1u = diff(cartpole_sym[3],x1,u)
d2f4_x2u = diff(cartpole_sym[3],x2,u)
d2f4_x3u = diff(cartpole_sym[3],x3,u)
d2f4_x4u = diff(cartpole_sym[3],x4,u)

d2f1_u2 = diff(cartpole_sym[0],u,u)
d2f2_u2 = diff(cartpole_sym[1],u,u)
d2f3_u2 = diff(cartpole_sym[2],u,u)
d2f4_u2 = diff(cartpole_sym[3],u,u)

def create_Bx_sym():
    Bx_sym = Array([
        [d2f1_x1u, d2f1_x2u, d2f1_x3u, d2f1_x4u],
        [d2f2_x1u, d2f2_x2u, d2f2_x3u, d2f2_x4u],
        [d2f3_x1u, d2f3_x2u, d2f3_x3u, d2f3_x4u],
        [d2f4_x1u, d2f4_x2u, d2f4_x3u, d2f4_x4u]])[:,:,0]  
    return Bx_sym

def create_Au_sym(): 
    Au_sym = Array([
        [d2f1_x1u],
        [d2f2_x1u],
        [d2f3_x1u],
        [d2f4_x1u],
        [d2f1_x2u],
        [d2f2_x2u],
        [d2f3_x2u],
        [d2f4_x2u],
        [d2f1_x3u],
        [d2f2_x3u],
        [d2f3_x3u],
        [d2f4_x3u],
        [d2f1_x4u],
        [d2f2_x4u],
        [d2f3_x4u],
        [d2f4_x4u]])[:,:,0]
    return Au_sym

def create_Bu_sym():
    Bu_sym = Array([ 
        [d2f1_u2],
        [d2f2_u2],
        [d2f3_u2],
        [d2f4_u2]])[:,:,0]
    return Bu_sym


Ax_sym = create_Ax_sym()
Bx_sym = create_Bx_sym()
Au_sym = create_Au_sym()
Bu_sym = create_Bu_sym()

dAdx = lambdify((x1,x2,x3,x4,u), Ax_sym)
dBdx = lambdify((x1,x2,x3,x4,u), Bx_sym)
dAdu = lambdify((x1,x2,x3,x4,u), Au_sym)
dBdu = lambdify((x1,x2,x3,x4,u), Bu_sym)

# function to compute hessian for all cases
def cartpole_hessian_rk4(x,u,s='dadx'):
    
    if s == 'dadx':
        xdd_1 = np.zeros((16,4)) # initial hessian for dAdx
        hfunc = dAdx
    elif s == 'dbdx':
        xdd_1 = np.zeros((4,4))
        hfunc = dBdx
    elif s == 'dadu':
        xdd_1 = np.zeros((16,1))
        hfunc = dAdu
    else: # 'dbdu' or anything else
        xdd_1 = np.zeros((4,1))
        hfunc = dBdu
    f1 = cartpole(x,u).flatten()  # value output of 
    d2f1 = hfunc(x[0],x[1],x[2],x[3],u) # d2f1 is 16x4 matrix

    x_2 = x + 0.5*h*f1 # update x for 2nd cartpole() call
    f2 = cartpole(x_2,u).flatten()
    d2f2 = hfunc(x_2[0],x_2[1],x_2[2],x_2[3],u)

    x_3 = x + 0.5*h*f2
    f3 = cartpole(x_3,u).flatten()
    d2f3 = hfunc(x_3[0],x_3[1],x_3[2],x_3[3],u)

    x_4 = x + 0.5*h*f3
    f4 = cartpole(x_4,u).flatten()
    d2f4 = hfunc(x_4[0],x_4[1],x_4[2],x_4[3],u)
    d2ft = xdd_1 + (h/6.0)*(d2f1 + 2*d2f2 + 2*d2f3 + d2f4)
    
    return d2ft 