import numpy as np
import sympy as sp
from IPython.display import display, Math

#Defining Vectors

ketV = sp.Matrix([0,1])
ketH = sp.Matrix([1,0])

ketD = sp.Matrix([1,1])
ketA = sp.Matrix([1,-1])
ketR = sp.Matrix([1,sp.I])
ketL = sp.Matrix([1,-sp.I])

#Defining Gates
# Identity gate (I)
I = sp.Matrix([[1, 0], [0, 1]])

# Pauli-X gate (X)
X = sp.Matrix([[0, 1], [1, 0]])

# Phase gate (S)
S = sp.Matrix([[1, 0], [0, sp.I]])

# Pauli-Y gate (Y)
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])

# T gate (T)
T = sp.Matrix([[1, 0], [0, sp.exp(sp.I * sp.pi / 4)]])
T_dagger = sp.Matrix([[1, 0], [0, sp.exp(-sp.I * sp.pi / 4)]])
# Hadamard gate (H)
H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)

# Projection gate (P_0)
P_0 = sp.Matrix([[1, 0], [0, 0]])

# Pauli-Z gate (Z)
Z = sp.Matrix([[1, 0], [0, -1]])

# Conjugate transpose of the Phase gate (S^dagger)
S_dagger = sp.Matrix([[1, 0], [0, -sp.I]])
class Photon():
    H = sp.Rational(1)/sp.sqrt(2)*sp.Matrix([[1,1],[1,-1]])
    Sdag = sp.Matrix([[1,0],[0,-sp.I]])
    S = sp.Matrix([[1,0],[0,sp.I]])
    def __init__(self, polarization = 'HV', amplitudes = sp.Matrix([1,0]),direction = None):
        self.polarization = polarization
        self.amplitudes = amplitudes
        self.direction = direction
        if(self.polarization=='HV'):
            self.digital = self.amplitudes
        elif(self.polarization=='DA'):
            self.digital = self.H*self.amplitudes
        elif(self.polarization=='RL'):
            self.digital = H*S_dagger*self.amplitudes
    def convertHV(self):
        direction_symbol = ''
        if(self.direction == '|'):
            direction_symbol = '\\downarrow ,'
        elif(self.direction == '-'):
            direction_symbol = '\\rightarrow ,'
        HVamplitude = self.digital
        amplitude_0 = sp.simplify(HVamplitude[0])
        amplitude_1 = sp.simplify(HVamplitude[1])
        latex_code = f"|{direction_symbol} \\psi \\rangle = \\left({sp.latex(amplitude_0)}\\right)|H\\rangle + \\left({sp.latex(amplitude_1)}\\right)|V\\rangle"
        display(Math(latex_code))
        return Photon('HV',self.digital,self.direction)
    def convertDA(self):
        direction_symbol = ''
        if(self.direction == '|'):
            direction_symbol = '\\downarrow ,'
        elif(self.direction == '-'):
            direction_symbol = '\\rightarrow ,'
        DAamplitude = self.H*self.digital
        amplitude_0 = sp.simplify(DAamplitude[0])
        amplitude_1 = sp.simplify(DAamplitude[1])

        latex_code = f"|{direction_symbol} \\psi \\rangle = \\left({sp.latex(amplitude_0)}\\right)|D\\rangle + \\left({sp.latex(amplitude_1)}\\right)|A\\rangle"
        display(Math(latex_code))
        return Photon('DA',DAamplitude,self.direction)
    def convertRL(self):
        direction_symbol = ''
        if(self.direction == '|'):
            direction_symbol = '\\downarrow ,'
        elif(self.direction == '-'):
            direction_symbol = '\\rightarrow ,'
        RLamplitude = self.S*self.H*self.digital
        amplitude_0 = sp.simplify(RLamplitude[0])
        amplitude_1 = sp.simplify(RLamplitude[1])

        latex_code = f"|{direction_symbol} \\psi \\rangle = \\left({sp.latex(amplitude_0)}\\right)|R\\rangle + \\left({sp.latex(amplitude_1)}\\right)|L\\rangle"
        display(Math(latex_code))
        return Photon('RL',RLamplitude,self.direction)
    def __mul__(self,gate):
        return Photon(self.polarization,gate*self.amplitudes,self.direction)
    def _repr_mimebundle_(self, **kwargs):
        direction_symbol = ''
        if(self.direction == '|'):
            direction_symbol = '\\downarrow ,'
        elif(self.direction == '-'):
            direction_symbol = '\\rightarrow ,'
        amplitude_0 = sp.simplify(self.digital[0])
        amplitude_1 = sp.simplify(self.digital[1])

        latex_code = f"|{direction_symbol} \\psi \\rangle = \\left({sp.latex(amplitude_0)}\\right)|0\\rangle + \\left({sp.latex(amplitude_1)}\\right)|1\\rangle"
        display(Math(latex_code))
    def visualize(self):
        direction_symbol = ''
        if(self.direction == '|'):
            direction_symbol = '\\downarrow ,'
        elif(self.direction == '-'):
            direction_symbol = '\\rightarrow ,'
        amplitude_0 = sp.simplify(self.digital[0])
        amplitude_1 = sp.simplify(self.digital[1])
        latex_code = f"|{direction_symbol} \\psi \\rangle = {sp.latex(amplitude_0)}|0\\rangle + {sp.latex(amplitude_1)}|1\\rangle"
        
        display(Math(latex_code))
    # add all the regular gates as things we can access, let's make the directional photon stuff
class beamSplitter():
    def __init__(self, A = None,B= None,r = None):

        self.A = A
        self.B = B

        if(r is None):
            self.r = sp.sqrt(B)
        else:
            self.r = r
    def apply(self, photon):
        if(photon.direction is None):
            print('No direction specified')
            return
        else:
            if(photon.direction == '-'):
                horzAmp = sp.sqrt(1-self.r**2)
                vertAmp = self.r
            elif(photon.direction == '|'):
                horzAmp = self.r
                vertAmp = -sp.sqrt(1-self.r**2)
                # then we wanna make two new photons, with the previous two photons amplitudes scaled by these new factors
            returnedHorzPhoton = Photon(photon.polarization, horzAmp*photon.amplitudes, '-')
            returnedVertPhoton = Photon(photon.polarization, vertAmp*photon.amplitudes, '|')
            return [returnedHorzPhoton, returnedVertPhoton]
# the beamsplitter class takes some input probabilities, or a value of r, and will return two photons depending
# on the direction of the incoming photon
class halfWavePlate():
    def __init__(self,theta):
        self.theta = theta
    def apply(self,photon):
        if(photon.direction is None):
            print('No direction specified')
            return
        else:
            return Photon(photon.polarization, sp.exp(sp.I*self.theta)*photon.amplitudes, photon.direction)
# the half wave plate class takes an angle, and will return a photon with the amplitudes rotated by that angle