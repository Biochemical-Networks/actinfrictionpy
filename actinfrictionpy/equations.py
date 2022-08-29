"""Implementation of overdamped equations of motion."""

import collections
import math

import numpy as np
from scipy import constants


ParamsRing = collections.namedtuple(
    "ParamsRing",
    [
        "k01",
        "r01",
        "r10",
        "r12",
        "r21",
        "deltas",
        "deltad",
        "k",
        "T",
        "Nf",
        "Nsca",
        "EI",
        "Lf",
        "r0",
        "KsD",
        "KdD",
        "cX",
        "tend",
        "lambda0",
        "Ndtot0",
    ],
)


ParamsLinear = collections.namedtuple(
    "ParamsLinear",
    [
        "k01",
        "r01",
        "r10",
        "r12",
        "r21",
        "deltas",
        "deltad",
        "k",
        "T",
        "r0",
        "Fcond",
    ],
)


def zeta0(p):
    return (
        constants.k
        * p.T
        / p.deltas**2
        / p.r0
        * np.sqrt(1 + 3 * p.k * p.deltas**2 / 4 / constants.k / p.T)
    )


def bending_force(lmbda, p):
    F = 8 * math.pi**3 * p.EI * p.Lf * p.Nf / p.Nsca**3
    G = -(p.deltas**3)
    H = 3 * p.Lf * p.deltas**2
    J = -3 * p.Lf**2 * p.deltas
    K = p.Lf**3

    return F / (G * lmbda**3 + H * lmbda**2 + J * lmbda + K)


def condensation_force(p):
    M = (
        -2
        * math.pi
        * constants.k
        * p.T
        * (2 * p.Nf - p.Nsca)
        / (p.Nsca * p.deltad)
        * np.log(1 + p.KsD**2 * p.cX / (p.KdD * (p.KsD + p.cX) ** 2))
    )

    return M


def entropic_force(lmbda, Nd, p):
    overlaps = 2 * p.Nf - p.Nsca
    logarg = 1 - Nd / ((1 + p.deltas / (p.deltad * overlaps) * lmbda) * overlaps)

    return overlaps * constants.k * p.T * np.log(logarg) / p.deltad


def friction_coefficient_linear_cX(lmbda, p):
    zs = p.r01 / p.r10
    zd = p.r01 * p.r12 / (p.r10 * p.r21)
    z = zd / (1 + zs) ** p.k
    rhos = (zs + zs**2) / ((1 + zs) ** 2 + zd)
    rhod = z / (1 + z)
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    C = (z + 1) / (z * np.exp(-B * np.exp((rhod + rhos) / (4 * B))) + 1)

    return zeta0(p) * C ** (1 + p.deltas / p.deltad * lmbda)


def friction_coefficient_linear_Nd(lmbda, Nd, p):
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    innerexp = Nd / ((1 + p.deltas / p.deltad * lmbda) * 4 * B)

    return zeta0(p) * np.exp(Nd * B * np.exp(innerexp))


def friction_coefficient_ring_cX(lmbda, p):
    zs = p.r01 / p.r10
    zd = p.r01 * p.r12 / (p.r10 * p.r21)
    z = zd / (1 + zs) ** 2
    rhos = (zs + zs**2) / ((1 + zs) ** 2 + zd)
    rhod = z / (1 + z)
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    C = (z + 1) / (z * np.exp(-B * np.exp((rhod + rhos) / (4 * B))) + 1)

    return zeta0(p) * C ** ((1 + p.deltas / p.deltad * lmbda) * (2 * p.Nf - p.Nsca))


def friction_coefficient_ring_Nd(lmbda, Nd, p):
    overlaps = 2 * p.Nf - p.Nsca
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    innerexp = Nd / ((1 + p.deltas / (p.deltad * overlaps) * lmbda) * overlaps * 4 * B)

    return zeta0(p) * np.exp(Nd * B * np.exp(innerexp))


def equation_of_motion_linear_cX(t, lmbda, p):
    zeta = friction_coefficient_linear_cX(lmbda, p)

    return p.Fcond / (p.deltas * zeta)


def equation_of_motion_linear_Nd(t, y, p):
    zeta = friction_coefficient_linear_Nd(y[0], y[1], p)

    dlmbda_dt = entropic_force(y[0], y[1], p) / (p.deltas * zeta)
    ltot = 1 + p.deltas / p.deltad * y[0]
    dN_dt = p.cX * p.k01 * p.r12 * ltot - (p.cX * p.k01 * p.r12 - p.r21 * p.r10) * y[1]

    return [dlmbda_dt, dN_dt]


def equation_of_motion_ring_cX(t, lmbda, p):
    zeta = friction_coefficient_ring_cX(lmbda, p)
    forcetot = bending_force(lmbda, p) + condensation_force(p)

    return -forcetot / (zeta * p.deltas * (2 * p.Nf - p.Nsca))


def equation_of_motion_ring_Nd(t, y, p):
    zeta = friction_coefficient_ring_Nd(y[0], y[1], p)
    forcetot = bending_force(y[0], p) + entropic_force(y[0], y[1], p)
    ltot = (1 + p.deltas / p.deltad * y[0]) * (2 * p.Nf - p.Nsca)
    dlmbda_dt = -forcetot / (zeta * p.deltas * (2 * p.Nf - p.Nsca))
    dN_dt = p.cX * p.k01 * p.r12 * ltot - (p.cX * p.k01 * p.r12 - p.r21 * p.r10) * y[1]

    return [dlmbda_dt, dN_dt]


def calc_equilibrium_ring_radius(p) -> float:
    """Calculate the equilibrium radius of a ring analytically."""
    num = p.EI * p.Nf * p.deltad * p.Lf * p.Nsca
    denom = (
        2
        * math.pi
        * p.T
        * constants.k
        * np.log(1 + p.KsD**2 * p.cX / (p.KdD * (p.KsD + p.cX) ** 2))
        * (2 * p.Nf - p.Nsca)
    )

    return (num / denom) ** (1 / 3)
