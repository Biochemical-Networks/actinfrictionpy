"""Implementation of overdamped equations of motion."""

import math

import numpy as np
from recordclass import recordclass
from scipy import constants


ParamsRing = recordclass(
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
        "Df",
        "eta",
        "Ds",
        "n",
        "KsD",
        "KdD",
        "cX",
        "tend",
        "lambda0",
        "Ndtot0",
    ],
)


ParamsLinear = recordclass(
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


ParamsHarmonicOscillator = recordclass(
    "ParamsHarmonicOscillator",
    [
        "gamma0",
        "k",
        "T",
    ],
)


def l_to_lambda(l, p):
    """Convert from continuous number of sites in an overlap to lambda."""
    return (l - 1) * p.deltad / p.deltas


def lambda_to_l(lmbda, p):
    """
    Convert from lambda to continuous number of sites in an overlap.
    """
    return 1 + p.deltas / p.deltad * lmbda


def lambda_to_l_discrete(lmbda, p):
    """
    Convert from lambda to discrete number of sites in an overlap.
    """
    return math.floor(p.deltas / p.deltad * lmbda) + 1


def lambda_to_R(lmbda, p):
    """Convert from ring radius to lambda."""
    return p.Nsca / (2 * math.pi) * (p.Lf - p.deltas * lmbda)


def R_to_lambda(R, p):
    """Convert from ring radius to lambda."""
    return 1 / p.deltas * (p.Lf - 2 * math.pi * R / p.Nsca)


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


def calc_equilibrium_occupancy(p) -> float:
    """Calculate the equilibrium occupancy."""
    xi_d = p.cX / p.KdD
    xi_s = p.cX / p.KsD

    return xi_d / ((1 + xi_s) ** 2 + xi_d)
