import numpy as np
from numpy import sin, sqrt, exp, cos, pi
from numpy.random import default_rng, SeedSequence
import multiprocessing
import concurrent.futures

class MultithreadedRNG:
    def __init__(self, n, seed=None, threads=None):
        if threads is None:
            threads = multiprocessing.cpu_count()
        self.threads = threads

        seq = SeedSequence(seed)
        self._random_generators = [default_rng(s)
                                   for s in seq.spawn(threads)]

        self.n = n
        self.executor = concurrent.futures.ThreadPoolExecutor(threads)
        self.values = np.empty(n)
        self.step = np.ceil(n / threads).astype(np.int_)

    def fill(self):
        def _fill(random_state, out, first, last):
            random_state.random(out=out[first:last])

        futures = {}
        for i in range(self.threads):
            args = (_fill,
                    self._random_generators[i],
                    self.values,
                    i * self.step,
                    (i + 1) * self.step)
            futures[self.executor.submit(*args)] = i
        concurrent.futures.wait(futures)

    def __del__(self):
        self.executor.shutdown(False)


#numPart = 25
#dominio = [(1, 7)]
#particulas = [np.random.rand(25)]
#maxGer = 50
#vMin = None
#vMax = None

class Enxame():
    def __init__(self, numPart, D:list[tuple], funcao, criterio, maxGer=100, 
                 inercia=0.5, cogn=2, soc = 1,
                 vLim:list[tuple] = None, max = True) -> None:
        self.numPart = numPart
        self.D = D
        self.dim = len(D)
        self.maxGer = maxGer
        self.vLim = vLim
        self.funcao = funcao
        self.criterio = criterio
        self.maxf = max

        #inicializar já pronto pro loop
        gerador = MultithreadedRNG(self.numPart*self.dim)
        gerador.fill()
        self.partPos = np.copy(
            (gerador.values *20 -10)
            .reshape((numPart, self.dim)))
        del gerador

        self.partVel = np.zeros_like(self.partPos, dtype=self.partPos.dtype)
        self.pbs = np.copy(self.partPos)
        
        if self.maxf:
            self.gb = self.partPos[np.argmax(
                np.apply_along_axis(funcao, axis=1, arr=self.partPos))]
        else:
            self.gb = self.partPos[np.argmin(
                np.apply_along_axis(funcao, axis=1, arr=self.partPos))]

        self.inercia = inercia
        self.cogn = cogn
        self.soc = soc
    
    def loop(self):
        ger = 0
        while (ger < self.maxGer) and not (self.criterio(self.partPos)):
            self.atualizar()
            self.avaliar()
            ger = ger+1
        #print(f"Loop efetuado em {ger} gerações")
    """Atualização dos recordes pessoais e global"""
    def avaliar(self):
        if self.maxf:
            for i, particula in enumerate(self.partPos):
                vAtual = self.funcao(particula)
                if vAtual > self.funcao(self.pbs[i]):
                    self.pbs[i] = particula
                    if vAtual > self.funcao(self.gb):
                        self.gb = particula
        else:
            for i, particula in enumerate(self.partPos):
                vAtual = self.funcao(particula)
                if vAtual < self.funcao(self.pbs[i]):
                    self.pbs[i] = particula
                    if vAtual < self.funcao(self.gb):
                        self.gb = particula
        print(f"{self.funcao(self.gb)},\t{self.gb[0]},\t{self.gb[1]}")
    """Atualização e normalização das velocidades e posições"""
    def atualizar(self):
        gerador = MultithreadedRNG(self.dim)
        gerador.fill()
        fa1 = np.ndarray.copy(gerador.values)
        gerador.fill()
        fa2 = np.ndarray.copy(gerador.values)
        del gerador #só pra liberar threads asap
        
        self.partVel = self.partVel*self.inercia + \
            self.cogn*fa1*(self.pbs - self.partPos) + \
            self.soc*fa2*(self.gb - self.partPos)
        
        def __normV(vec):
            for index, elemento in enumerate(vec):
                #checando se é menor que o max
                if self.vLim[index][1] < elemento: 
                    elemento = self.vLim[index][1] 
                    continue
                if self.vLim[index][0] > elemento:
                    elemento = self.vLim[index][0]
            return vec

        if self.vLim != None:
            self.partVel = np.apply_along_axis(__normV, axis=1, arr=self.partVel)

        self.partPos = self.partVel + self.partPos

        def __normP(vec):
            newVec = np.copy(vec)
            for index, elemento in enumerate(vec):
                #checando se é menor que o max
                if self.D[index][1] < elemento: 
                    newVec[index] = self.D[index][1] 
                    continue
                if self.D[index][0] > elemento:
                    newVec[index] = self.D[index][0]
            return newVec

        self.partPos = np.apply_along_axis(__normP, axis=1, arr=self.partPos)

       

#teste = np.array([1,2,3], dtype=np.int64)
#teste2 = np.array([[1,1,1],[10,10,10],[100,100,100]], dtype=np.int64)
#print(teste-teste2)

#dominio = ((np.float64(-10.0), np.float64(10.0)), (np.float64(-10000.0), np.float64(100000.0)))
#dominio = [(np.float64(-10.0), np.float64(10.0))]
#funcao = lambda x : x*x - 3*x + 4
#fcrit = lambda posMatrix : np.std(posMatrix) < 0.2
#teste = Enxame(25, dominio, funcao, fcrit, 10)
#
#print(teste.partPos)
#temp = np.copy(teste.partPos)
#print(teste.gb)
#print(teste.funcao(teste.gb))
#
#print("-"*80)
#
#teste.loop()
#print(teste.partPos)
#print(teste.gb)
#print(teste.funcao(teste.gb))



'''
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

numPart = 10
Dominio = [(np.float32(-500.0),np.float32(500.0)), (np.float32(-500.0),np.float32(500.0))]
criterio = lambda a : False
#blau = Enxame(numPart, Dominio, w27, criterio, soc=1, max=False)
blau = Enxame(numPart, Dominio, funcao=w27, criterio=criterio,soc=2, max=False,
    maxGer=500)
blau.loop()

#print(blau.partPos)
#print(blau.gb)
#print(blau.funcao(blau.gb))
'''