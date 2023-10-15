from numpy import sin, sqrt, exp, cos, pi
from Enxame import *
import matplotlib.pyplot as plt

a = 500
b = 0.1
c = pi/2
x1 = lambda x : 25*x
x2 = lambda y : 25*y
F10 = lambda x : -a * exp(-b * sqrt( (x1(x[0])**2 + x2(x[1])**2) /2) ) - \
    exp((cos(c*x1(x[0])) + cos(c*x2(x[1]))) /2) + exp(1)
zsh = lambda x : 0.5 - (( sin( sqrt(x[0]**2 + x[1]**2) )**2 ) -0.5)/ \
    ((1 + 0.1* (x[0]**2 + x[1]**2) )**2)
Fobj = lambda x : F10(x)*zsh(x)
r = lambda x : 100*(x[1] - x[0]*x[0])**2 + (1 - x[0])**2
rd = lambda x : 1 + (x[1] - x[0]**2)**2 + (1-x[0])**2
z = lambda x : x[0]*sin(sqrt(abs(x[0]))) - x[1]*sin(sqrt(abs(x[1])))
w4 = lambda x : sqrt(r(x)**2 + z(x)**2)+Fobj(x)
w23 = lambda x : z(x)/rd(x)
w27 = lambda x : w4(x) + w23(x)

if __name__ == "__main__":
    numPart = 10
    Dominio = [(np.float32(-500.0),np.float32(500.0)), (np.float32(-500.0),np.float32(500.0))]
    criterio = lambda a : False
    teste = Enxame(numPart, Dominio, funcao=w27, criterio=criterio,soc=2, max=False,
        maxGer=100)
    teste.loop()

#Npts = 5000
#d = (-500, 500)
#x = np.linspace(d[0],d[1], Npts)
#y = np.linspace(d[0],d[1], Npts)
#X, Y = np.meshgrid(x, y, sparse=True)
#Z = w27([X,Y])
#
#print(Z.min())
#plt.contourf(x, y, np.log10(Z + np.abs(Z.min()) +1))
#plt.axis('scaled')
#plt.colorbar()
#plt.show()
#res = w27