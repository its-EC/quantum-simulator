import numpy as np
from numpy.polynomial import hermite
from numerical import *

class QuantumSystem:
    def __init__(self, mass, hbar, L, points=1001):
        self.mass = mass
        self.hbar = hbar
        self.points = points
        self.L = L

    def psi(self, n, x):
        raise NotImplementedError("Wavefunction not defined yet")

    def prob_density(self, n, x=None):
        return np.abs(self.psi(n, x)**2)

    def energy(self, n):
        raise NotImplementedError("Energy not defined yet")

    def nodes(self, n):
        raise NotImplementedError("Nodes not defined yet")

    def range(self, n):
        ymax1 = 0
        ymax2 = 0
        for x in range(n, 21):
            y1 = self.psi(n)
            y2 = self.prob_density(n)
            ymax1 = max(ymax1, np.max(np.abs(y1)))
            ymax2 = max(ymax2, np.max(np.abs(y2)))
        limits = [(ymax1 * 1.5), (ymax2 * 1.5)]
        return limits

    def integral(self, n):
        return simpson(self.prob_density(n), self.x, self.points)

class ParticleInBox(QuantumSystem):
    def __init__(self, mass, hbar, L, points=1001):
        super().__init__(mass, hbar, L, points)
        self.x = np.linspace(0, self.L, points)
        self.lower = 0
        self.upper = self.L

    def psi(self, n ,x=None):
        x = self.x
        return np.sqrt(2 / self.L) * np.sin(n * np.pi * x / self.L)

    def energy(self, n):
        return (n**2 * self.hbar**2 * np.pi**2) / (2 * self.mass * self.L**2)

    def nodes(self, n):
        return n - 1

    def range(self, n):
        limits = [1.5*np.sqrt(2/self.L), 1.5*2/self.L]
        return limits

class ParticleInFreeSpace(QuantumSystem):
    def __init__(self, mass, hbar, L, points=1001):
        super().__init__(mass, hbar, L, points)
        self.x = np.linspace(-self.L, self.L, points)
        self.lower = -self.L
        self.upper = self.L

    def psi(self, k ,x=None):
        x = self.x
        return np.cos(-k * x) + 1j * -np.sin(-k * x)

    def energy(self, k):
        return (k**2 * self.hbar**2) / (2 * self.mass)

    def nodes(self, n):
        return 0

    def range(self, n):
        limits = [1.5*1, 1.5*1]
        return limits

class HarmonicOscillator(QuantumSystem):
    def __init__(self, mass, hbar, L,  points=1001, omega=1e15):
        super().__init__(mass, hbar, L, points)
        self.x = np.linspace(-self.L, self.L, points)
        self.omega = omega
        self.lower = -self.L
        self.upper = self.L

    def psi(self, n, x=None):
        x = self.x
        coeffs = [0] * n + [1]
        return (1/((2**n * np.prod(range(1, n+1))) ** (1/2))
            * ((self.mass * self.omega)/(np.pi * self.hbar)) ** (1/4)
            * np.exp(-(self.mass * self.omega)/(2 * self.hbar) * x**2)
            * hermite.hermval((self.mass * self.omega/self.hbar) ** (1/2) * x, coeffs))

    def energy(self, n):
        return self.hbar * self.omega * (n + 1/2)

    def nodes(self, n):
        return n