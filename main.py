from systems import ParticleInBox, ParticleInFreeSpace
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy.constants import hbar, m_e, m_p, m_n, electron_volt

def choose_system():
    choice_system = int(input("Enter the number corresponding to your quantum system."
                       "\n1: Particle in 1D box"
                       "\n2: Particle in free space"
                       "\n3: Harmonic Oscillator \n"))

    systems = {
        1: ParticleInBox,
        2: ParticleInFreeSpace,
        3: ParticleInBox
    }

    return systems[choice_system]

def choose_mass():
    choice_mass = int(input("Enter the number corresponding to your particle."
                       "\n1: Electron"
                       "\n2: Proton"
                       "\n3: Neutron"
                       "\n4: Other \n"))
    particles = {
        1: m_e,
        2: m_p,
        3: m_n,
    }
    if choice_mass == 4:
        mass = int(input("Enter the mass of the particle in kg."))
        return mass
    else:
        return particles[choice_mass]


def plot_graph(quantum_system):
    fig, (axis1, axis2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, sharey=True)
    plt.subplots_adjust(bottom=0.25)
    x = quantum_system.x

    if np.iscomplexobj(quantum_system.psi(n)):
        line1_real, = axis1.plot(x, quantum_system.psi(n).real, 'blue', label='Real')
        line1_imaginary, = axis1.plot(x, quantum_system.psi(n).imag, 'black', label='Imaginary')
    else:
        line1_real, = axis1.plot(x, quantum_system.psi(n).real, 'blue')

    line2, = axis2.plot(x, quantum_system.prob_density(n), 'red')

    axis1.set_title(f'Wavefunction, n = {n}')
    axis2.set_title(f'Probability Density Function, n = {n}')

    axis1.set_ylabel('$\psi(x)$')
    axis2.set_ylabel('$|\psi(x)^2|$')

    axis1.set_xlabel('x')
    axis2.set_xlabel('x')

    axis1.set_xlim(-10, quantum_system.L)
    axis1.set_ylim(-2.25, 2.25)

    axis1.axhline(0, color='grey', linestyle='--', alpha=0.3)
    axis2.axhline(0, color='grey', linestyle='--', alpha=0.3)

    axes_slider = plt.axes([0.2, 0.1, 0.6, 0.1])

    if system_type == ParticleInBox:
        slider = Slider(axes_slider, 'n', 1, 25, valinit=1, valstep=1, facecolor='g')
        axis1.set_title(f'Wavefunction, n = {n}')
        axis2.set_title(f'Probability Density Function, n = {n}')

    elif system_type == ParticleInFreeSpace:
        slider = Slider(axes_slider, 'k', 1, 25, valinit=1, valstep=1, facecolor='g')
        axis1.set_title(f'Wavefunction, k = {n}')
        axis2.set_title(f'Probability Density Function, k = {n}')

    def update(val):
        n = slider.val
        line1_real.set_ydata(quantum_system.psi(n).real)
        line1_imaginary.set_ydata(quantum_system.psi(n).imag)
        line2.set_ydata(quantum_system.prob_density(n))

        if system_type == ParticleInBox:
            axis1.set_title(f'Wavefunction, n = {n}')
            axis2.set_title(f'Probability Density Function, n = {n}')
        elif system_type == ParticleInFreeSpace:
            axis1.set_title(f'Wavefunction, k = {n}')
            axis2.set_title(f'Probability Density Function, k = {n}')
        fig.canvas.draw_idle()

    slider.on_changed(update)
    axis1.legend()
    plt.show()

n = 1
system_type = choose_system()
mass = choose_mass()
quantum_system = system_type(mass, hbar)
plot_graph(quantum_system)