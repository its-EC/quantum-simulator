import numpy as np

class QuantumSystem:
    def __init__(self, mass, hbar, points=1000):
        self.mass = mass
        self.hbar = hbar
        self.points = points

    def psi(self, n, x):
        raise NotImplementedError("Wavefunction not defined yet")

    def prob_density(self, n, x=None):
        return np.abs(self.psi(n, x)**2)

    def energy(self, n):
        raise NotImplementedError("Energy not defined yet")

    def nodes(self, n):
        return n - 1

class ParticleInBox(QuantumSystem):
    def __init__(self, mass, hbar, points=1000, L=1.0):
        super().__init__(mass, hbar, points)
        self.L = L
        self.x = np.linspace(0, L, points)

    def psi(self, n ,x=None):
        x = self.x
        return np.sqrt(2 / self.L) * np.sin(n * np.pi * x / self.L)

    def energy(self, n):
        return (n**2 * self.hbar**2 * np.pi**2) / (2 * self.mass * self.L**2)


class ParticleInFreeSpace(QuantumSystem):
    def __init__(self, mass, hbar, points=1000, L=10):
        super().__init__(mass, hbar, points)
        self.L = L
        self.x = np.linspace(-L, L, points)

    def psi(self, k ,x=None):
        x = self.x
        return np.cos(-k * x) + 1j * -np.sin(-k * x)

    def energy(self, k):
        return (k**2 * self.hbar**2) / (2 * self.mass)