#OKRESLENIE POZYCYJI WEZLOW
def x(n):
    if n == 1:
        x = -1.0
    if n == 2:
        x = -1.0 + A/2.
    return x

#ROZLOZENIE ATOMOW W SIECI 
def tablica(m):
    for i in range(1,m+1):
        for j in range(1,m+1):
            for k in range(1,m+1):
                for l in range(1,3):
                    X.append(x(l) + (i-1) *A + random.uniform(-0.1*A,0.1*A))
                    Y.append(x(l) + (j-1) *A + random.uniform(-0.1*A,0.1*A))
                    Z.append(x(l) + (k-1) *A + random.uniform((-0.1*A),(0.1*A)))
                    VX.append(random.uniform(-1.0*vmaxx,vmaxx))
                    VY.append(random.uniform(-1.0*vmaxx,vmaxx))
                    VZ.append(random.uniform(-1.0*vmaxx,vmaxx))
                    
def ektemp(EKX):
    EKX = 0
    for i in range(0,len(VX)):
        EKX += VX[i]*VX[i] + VY[i]*VY[i] + VZ[i]*VZ[i]
    EKX *= 0.5 / dtx2
    return EKX

def temperatura_z_ek(EKX):
    TemperaturaX = (2 * EKX) / (3 * (N - 1))
    Temperatura = (TemperaturaX * epsilonjoul) / Kb
    return Temperatura

def viscale():
    for i in range(0,len(VX)):
        VX[i] *= sc
        VY[i] *= sc
        VZ[i] *= sc

def newpositions():
    for t in range(0,N-1):
            X[t] += VX[t] + 0.5 * FX[t] * dtx2
            Y[t] += VY[t] + 0.5 * FY[t] * dtx2
            Z[t] += VZ[t] + 0.5 * FZ[t] * dtx2
    
            X[t] -= 2.0 * round(X[t]/2.0)
            Y[t] -= 2.0 * round(Y[t]/2.0)
            Z[t] -= 2.0 * round(Z[t]/2.0)

def newvelocities():
    for t in range(0,N-1):
        VX[t] += 0.5 * FX[t] * dtx2
        VY[t] += 0.5 * FY[t] * dtx2
        VZ[t] += 0.5 * FZ[t] * dtx2

def usuwanie_pedu():
    cx=0.0
    cy=0.0
    cz=0.0
    for i in range(0,len(X)):
        cx += VX[i]
        cy += VY[i]
        cz += VZ[i]
    
    cx /= N
    cy /= N
    cz /= N
    for i in range(0,len(X)):
        VX[i] -= cx
        VY[i] -= cy
        VZ[i] -= cz
        
def forces():
    EP = 0.0

    for k in range(0, N-1):
        FX[k] = 0.0
        FY[k] = 0.0
        FZ[k] = 0.0
        
    for i in range(0,N-2):
        xi=X[i]
        yi=Y[i]
        zi=Z[i]
        for j in range(i+1,N-1):
            xij = xi - X[j]
            xij -= 2 * round(xij/2.0) #konwencja najblizszych obrazow
            yij = yi - Y[j]
            yij -= 2 * round(yij/2.0)#konwencja najblizszych obrazow
            zij = zi - Z[j]
            zij -= 2 * round(zij/2.0)#konwencja najblizszych obrazow        
            rij2 = xij * xij + yij * yij + zij * zij
            #print("POKAZ RIJ2: ",rij2)    
            if(rij2 <= 1.0):
                SR2 = sigmax2 / rij2
                SR6 = SR2*SR2*SR2
                SR12 = SR6*SR6
                EP += SR12 - SR6
                FA = (2.0*SR12 - SR6)/rij2
                FX[i] +=  FA * xij
                FY[i] +=  FA * yij
                FZ[i] +=  FA * zij
                FX[j] -=  FA * xij
                FY[j] -=  FA * yij
                FZ[j] -=  FA * zij
    EP *= 4.0

    for i in range(0,len(FX)):
        FX[i] *= 24.0
        FY[i] *= 24.0
        FZ[i] *= 24.0 
		
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from math import *

X = []
Y = []
Z = []
VX = []
VY = []
VZ = []
FX = []
FY = []
FZ = []

EKX = 0
Temperatura = 0
EP = 0.0
cx = 0.0
cy = 0.0
cz = 0.0
Temp = 87.3# [K]
ro = 1394# [kg/m^3]
i = 0
j = 0
k = 0
M = 2
A = 2./float(M)
NA = 6.022045e23
Kb = 1.38066e-23
mar = 39.948 #[u]
dt = 1.0e-14 #sekundy
epsilon = 119.8 #kelvina
sigma = 3.41e-10 #metr
NEQ = 1000

mkg = mar / NA * 1e-3 #[kg]
N = 2 * M**3
L = (N * mkg / ro)**(1./3.) #[m * 1e-9]
H = L/2.
vmax = sqrt(3 * Kb * Temp / mkg)
epsilonjoul = epsilon * Kb
Tempx = Kb * Temp / epsilonjoul
dtx = dt * sqrt(epsilonjoul / (mkg * H * H))
dtx2 = dtx * dtx
vmaxx = sqrt(3 * Tempx) * dtx
sigmax = sigma / H
sigmax2 = sigmax * sigmax

#INICJALIZACJA SIATKI
tablica(M)

#PERIODYCZNE WARUNKI BRZEGOWE
for i in range(0,len(X)):
    X[i] -= 2.0 * round(X[i]/2.0)
    Y[i] -= 2.0 * round(Y[i]/2.0)
    Z[i] -= 2.0 * round(Z[i]/2.0)
    cx += VX[i]
    cy += VY[i]
    cz += VZ[i]
    FX.append(0.0)
    FY.append(0.0)
    FZ.append(0.0)


cx /= N
cy /= N
cz /= N

for i in range(0,len(X)):
    VX[i] -= cx
    VY[i] -= cy
    VZ[i] -= cz



EKX = ektemp(EKX)
Temperatura = temperatura_z_ek(EKX)
print("TEMPERATURA Z ENERGII KINETYCZNEJ: ", Temperatura)
sc = sqrt(Temp / Temperatura)
viscale()
EKX = ektemp(EKX)
Temperatura = temperatura_z_ek(EKX)
print("TEMPERATURA Z ENERGII KINETYCZNEJ PO SKALOWANIU: ", Temperatura)


forces()

SUM_A = 0.0
SUM_A2 = 0.0
#Rownania rozniczkowe
for i in range(0,NEQ):
    print(i)
    
    EKX = ektemp(EKX)
    Temperatura = temperatura_z_ek(EKX)
    
    print("TEMPERATURA Z ENERGII KINETYCZNEJ: ", Temperatura)
    
    sc = sqrt(Temp / Temperatura)
    if(abs(Temp-Temperatura)>1.0):
        viscale()
    EKX = ektemp(EKX)
    Temperatura = temperatura_z_ek(EKX)
    
    print("TEMPERATURA Z ENERGII KINETYCZNEJ PO SKALOWANIU: ", Temperatura)
    
    
    newpositions()
    newvelocities()
    forces()    
    newvelocities()



#fig = plt.figure()
#ax = Axes3D(fig)

#ax.scatter(X,Y,Z, c="goldenrod")
#plt.show()
