from tools import debug
from random import uniform
import numpy as np


class Simulation():
    def __init__(self, constants):
        self.c = constants

    def initialize_values(self):
        self.R = [[], [], []]
        self.V = [[], [], []]
        self.F = [[], [], []]
        self.Ep = 0

    def set_atoms(self, kom):
        for i in range(1, kom+1):
            for j in range(1, kom+1):
                for k in range(1, kom+1):
                    for l in range(1,3):
                        self.R[0].append(self.xyz(l) + (i-1)*self.c['A'] + self.rand())
                        self.R[1].append(self.xyz(l) + (j-1)*self.c['A'] + self.rand())
                        self.R[2].append(self.xyz(l) + (k-1)*self.c['A'] + self.rand())
                        self.V[0].append(self.rand(1))
                        self.V[1].append(self.rand(1))
                        self.V[2].append(self.rand(1))
        return None

    def xyz(self, foo):
        if foo == 1:
            return -1.
        if foo == 2:
            return -1 + self.c['A']
    
    def rand(self, flag=0):
        if flag == 1:
            return uniform(-self.c['v_rmax'], self.c['v_rmax'])
        else:
            return uniform(-0.1*self.c['A'], 0.1*self.c['A'])

    def w_brzegowe(self):
        c = [0, 0, 0]
        for i in range(self.c['M']):
            for j in range(3):
                self.R[j][i] -= 2*round(self.R[j][i]/2)
                self.F[j].append(0.)
                c[j] += self.V[j][i]
        c = [i/self.c['N'] for i in c]
        for i in range(self.c['M']):
            for j in range(3):
                self.V[j][i] -= c[j]
        return None


    def get_Ek(self):
        Ek = 0
        for i in range(self.c['M']):
            for j in range(3):
                Ek += self.V[j][i]**2
        return 0.5*Ek/self.c['dt_r2']

    def get_T(self, Ek):
        _T = 2*Ek/(3*(self.c['N']-1))
        return _T*self.c['eps_j']/self.c['K_b']
    
    def scale_V(self, T):
        scale = np.sqrt(self.c['T']/T)
        for i in range(self.c['M']):
            for j in range(3):
                self.V[j][i] *= scale
        return None

    def get_forces(self):
        self.Ep = 0
        for i in range(self.c['N']-1):
            for j in range(3):
                self.F[j][i] = 0.
        for i in range(self.c['N']-2):
            xi = self.R[0][i]
            yi = self.R[1][i]
            zi = self.R[2][i]
            for j in range(i+1, self.c['N']-1):
                xij = xi - self.R[0][j]
                xij -= 2*round(xij/2.)
                yij = yi - self.R[1][j]
                yij -= 2*round(yij/2.)
                zij = zi - self.R[2][j]
                zij -= 2*round(zij/2.)

                rij = xij**2 + yij**2 + zij**2
                #print(rij)
                if (rij <= 1.):
                    sr2 = self.c['sigma_r2']/rij
                    sr6 = sr2**3
                    sr12 = sr6**2
                    self.Ep += sr12 - sr6
                    f = (2*sr12 - sr6)/rij
                    self.F[0][i] += f*xij
                    self.F[1][i] += f*yij
                    self.F[2][i] += f*zij
                    self.F[0][j] -= f*xij
                    self.F[1][j] -= f*yij
                    self.F[2][j] -= f*zij
        self.Ep *= 4.
        for i in range(self.c['M']):
            for j in range(3):
                self.F[j][i] *= 24.0
        return None
        
    def set_pos(self):
        for i in range(self.c['N']-1):
            for j in range(3):
                self.R[j][i] += self.V[j][i] + 0.5*self.F[j][i]*self.c['dt_r2']
                self.R[j][i] -= 2.*round(self.R[j][i]/2.)
        return None

    def set_V(self):
        for i in range(self.c['N']-1):
            for j in range(3):
                self.V[j][i] += 0.5*self.F[j][i] * self.c['dt_r2']
    
    def run(self, time):
        for t in range(time):
            _Ek = self.get_Ek()
            _T = self.get_T(_Ek)
            print('T->{}'.format(self.V[0][1]))
            #=======================
            if (np.abs(self.c['T'] - _T)>1.):
                self.scale_V(_T)
            #_Ek = self.get_Ek()
            #_T = sel
            self.set_pos()
            self.set_V()
            self.get_forces()
            self.set_V()

    def initialize(self):
        self.initialize_values()
        self.set_atoms(self.c['N'])
        self.w_brzegowe()
        ek = self.get_Ek()
        t = self.get_T(ek)
        print("T->{}".format(t))
        self.scale_V(t)
        ek = self.get_Ek()
        t = self.get_T(ek)
        print("sc.T->{}".format(t))
        self.get_forces()
        print(self.c['v_rmax'])
