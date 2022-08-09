"""Plot types."""


import matplotlib.pyplot as plt

# from matplotlib import cm
# from matplotlib import ticker
# from matplotlibstyles import plotutils
# import numpy as np
# import pandas as pd
# from scipy import interpolate


class Plot:
    """Base class for all plot types.

    Attributes:
        f: Figure
        ax: Axis

    Methods:
        plot: Plot single timeseries
        plot_comparison: Plot multiple different timeseries
        plot_meanvar: Plot mean and variance
        setup_axis: Setup the axis, call after all plotting
        set_labels: Set labels, legend, colourbar
    """

    def __init__(self, f, ax):
        self._f = f
        self._ax = ax

    def set_labels(self):
        plt.legend()

    def plot_meanvar(self, t, mean, var, *args, **kwargs):
        self._ax.plot(t, mean, *args, **kwargs)
        self._ax.fill_between(
            t,
            mean - var**0.5,
            mean + var**0.5,
            color="0.8",
            zorder=0,
        )


class LambdaPlot(Plot):
    """Plot time series of lambda."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.lmbda, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(df_means.t, df_means.lmbda, df_vars.lmbda, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$\lambda$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class RadiusPlot(Plot):
    """Plot time series of ring radius in micro meters."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.R / 1e-6, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(df_means.t, df_means.R, df_vars.R, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$R / \si{\micro\meter}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class EquilibriumRadiusFractionPlot(Plot):
    """Plot time series of fraction of radius to equilibrium radius."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.R_eq_frac, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.R_eq_frac, df_vars.R_eq_frac, *args, **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\frac{R_\text{max} - R}{R_\text{max} - R_\text{eq}}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class NdtotPlot(Plot):
    """Plot time series of Ndtot."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.Ndtot, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(df_means.t, df_means.Ndtot, df_vars.Ndtot, *args, **kwargs)

    def setup_axis(self):
        self._ax.set_ylabel(r"$N_\text{d, tot}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class NdOccupancyPlot(Plot):
    """Plot time series of Nd occupancy."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.Nd_occupancy, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.Nd_occupancy, df_vars.Nd_occupancy, *args, **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$N_\text{d, occ}$")
        # self._ax.set_ylabel(r"$N_\text{d} / \ell_\text{tot}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class TotalForcePlot(Plot):
    """Plot time series of total force in pico Newtons."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.force_total / 1e-12, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.force_total / 1e-12,
            df_vars.force_total / 1e-12,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$F_\text{tot} / \si{\pico\newton}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class EntropicForcePlot(Plot):
    """Plot time series of entropic force in pico Newtons."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.force_entropy / 1e-12, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.force_entropy / 1e-12,
            df_vars.force_entropy / 1e-12,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$F_\text{ent} / \si{\pico\newton}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class ZetacXPlot(Plot):
    """Plot time series of cX friction coefficient."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.zeta_cX, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t, df_means.zeta_cX, df_vars.zeta_cX, *args, **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta_\text{cX}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class ZetaDoubleExpPlot(Plot):
    """Plot time series of double exponent friction coefficient."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.zeta_Nd_double_exp, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.zeta_Nd_double_exp,
            df_vars.zeta_Nd_double_exp,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta_\text{de}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class ZetaSingleExpPlot(Plot):
    """Plot time series of single exponent friction coefficient."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.zeta_Nd_single_exp, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.zeta_Nd_single_exp,
            df_vars.zeta_Nd_single_exp,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta_\text{se}$")


class ZetaContinuouslPlot(Plot):
    """Plot time series of continuous l friction coefficient."""

    def plot(self, df, *args, **kwargs):
        self._ax.plot(df.t, df.zeta_continuous_l, *args, **kwargs)

    def plot_meanvar(self, df_means, df_vars, *args, **kwargs):
        super().plot_meanvar(
            df_means.t,
            df_means.zeta_continuous_l,
            df_vars.zeta_continuous_l,
            *args,
            **kwargs
        )

    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta_\text{cl}$")
        self._ax.set_xlabel(r"$t / \si{\second}$")


class AllZetaPlot(Plot):
    """Plot time series of each type of friction coefficient"""

    def plot_comparison(self, dfs, colors, *args, **kwargs):
        self._ax.plot(dfs[0].t, dfs[0].zeta_cX, color=colors[0], *args, **kwargs)
        self._ax.plot(
            dfs[1].t, dfs[1].zeta_Nd_double_exp, color=colors[1], *args, **kwargs
        )
        self._ax.plot(
            dfs[2].t, dfs[2].zeta_Nd_single_exp, color=colors[2], *args, **kwargs
        )
        super().plot_meanvar(
            dfs[3][0].t,
            dfs[3][0].zeta_continuous_l,
            dfs[3][1].zeta_continuous_l,
            color=colors[3],
            *args,
            **kwargs
        )
    def setup_axis(self):
        self._ax.set_ylabel(r"$\zeta$")
        self._ax.set_xlabel(r"$t / \si{\second}$")
