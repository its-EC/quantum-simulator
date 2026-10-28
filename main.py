from systems import ParticleInBox, ParticleInFreeSpace, HarmonicOscillator
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy.constants import hbar, m_e, m_p, m_n, electron_volt

def choose_system():
    choice_system = int(input("Enter the number corresponding to your quantum system."
                       "\n1: Particle in a 1D box"
                       "\n2: Particle in free space"
                       "\n3: Harmonic Oscillator \n"))

    systems = {
        1: ParticleInBox,
        2: ParticleInFreeSpace,
        3: HarmonicOscillator
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
    fig, (axis1, axis2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, sharey=False)
    plt.subplots_adjust(bottom=0.25, hspace=0.3)
    x = quantum_system.x
    x_nm = x*(1e9)

    if np.iscomplexobj(quantum_system.psi(n)):
        line1_real, = axis1.plot(x_nm, quantum_system.psi(n).real, "blue", label="Real")
        line1_imaginary, = axis1.plot(x_nm, quantum_system.psi(n).imag, "black", label="Imaginary")
    else:
        line1_real, = axis1.plot(x_nm, quantum_system.psi(n).real, "blue")

    line2, = axis2.plot(x_nm, quantum_system.prob_density(n), "red")

    axis1.set_ylabel("$\psi(x)$")
    axis2.set_ylabel("$|\psi(x)^2|$")

    axis1.set_xlabel('x/nm')
    axis2.set_xlabel('x/nm')

    limits = quantum_system.range(n)
    axis1.set_xlim(quantum_system.lower*1e9, quantum_system.upper*1e9)
    axis1.set_ylim(-limits[0], limits[0])
    axis2.set_ylim(-limits[1], limits[1])

    axis1.axhline(0, color="grey", linestyle="--", alpha=0.3)
    axis2.axhline(0, color="grey", linestyle="--", alpha=0.3)

    axes_slider = plt.axes([0.2, 0.05, 0.6, 0.1])


    if system_type == ParticleInFreeSpace:
        slider = Slider(axes_slider, "k", 1e8, 1e9, valinit=1e8, valstep=1e6, facecolor="g")
        axis1.set_title(f"Wavefunction, k = {n}")
        axis2.set_title(f"Probability Density Function, k = {n}")

    else:
        slider = Slider(axes_slider, "n", n, 20, valinit=n, valstep=1, facecolor="g")
        axis1.set_title(f"Wavefunction, n = {n}")
        axis2.set_title(f"Probability Density Function, n = {n}")

    text = fig.text(
        0.5, 0.15,
        "",
        ha="center", va="center",
        fontsize=12,
        bbox=dict(boxstyle="round", facecolor="#f0f0f0", edgecolor="grey")
    )

    def update(val):
        n = slider.val
        energy = quantum_system.energy(n)/electron_volt
        nodes = quantum_system.nodes(n)
        integral = quantum_system.integral(n)

        if np.iscomplexobj(quantum_system.psi(n)):
            line1_real.set_ydata(quantum_system.psi(n).real)
            line1_imaginary.set_ydata(quantum_system.psi(n).imag)
            line2.set_ydata(quantum_system.prob_density(n))
        else:
            line1_real.set_ydata(quantum_system.psi(n).real)
            line2.set_ydata(quantum_system.prob_density(n))

        if system_type == ParticleInFreeSpace:
            axis1.set_title(f"Wavefunction, k = {n}")
            axis2.set_title(f"Probability Density Function, k = {n}")
            text.set_text(f"k = {n}   |   E = {energy:.3E} eV   |   Nodes = {nodes} | Probability Integral = {integral:.3E}")

        else:
            axis1.set_title(f"Wavefunction, n = {n}")
            axis2.set_title(f"Probability Density Function, n = {n}")
            text.set_text(f"n = {n}   |   E = {energy:.3E} eV   |   Nodes = {nodes} | Probability Integral = {integral:.3E}")

        fig.canvas.draw_idle()

    slider.on_changed(update)
    axis1.legend(loc="upper right")
    plt.show()


system_type = choose_system()
mass = choose_mass()
L = float(input("What length (in nm) do you want to see across?"))/1e9

if system_type == HarmonicOscillator:
    n = 0
elif system_type == ParticleInFreeSpace:
    n = 1e8
else:
    n = 1

quantum_system = system_type(mass, hbar, L)
plot_graph(quantum_system)