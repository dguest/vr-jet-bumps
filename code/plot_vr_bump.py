#!/usr/bin/env python3

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import os

def frac(pt, c=1, rho=30, rmax=0.4):
    vr_frc = c + (1-c) * rho**2 / (pt * rmax)**2
    return np.minimum(1.0, vr_frc)

def fprime(pt, c=1, rho=30, rmax=0.4):
    vr_fp = (1-c) * (-2 * rho**2) / (pt * rmax)**3
    flat = pt < rho / rmax
    vr_fp[flat] = 0
    return vr_fp

def diff(pt, c=1, rho=30, rmax=0.4):
    f = frac(pt, c, rho, rmax)
    fp = fprime(pt, c, rho, rmax)
    df = 1 / f * (1 - fp * pt / f)
    return df

def psmooth(pt, c=1, rho=30, rmax=0.4):
    return pt / frac(pt, c, rho, rmax)

def dress(ax, ylab=None):
    ax.set_xlabel(r'$p_{\rm T}$ [GeV]', x=0.98, ha='right')
    ax.set_ylabel(ylab or 'Arb')
    ax.legend(title='containment')

def make_plots(plots='figures'):
    dims = (5,3)
    frac_fig = Figure(dims)
    FigureCanvas(frac_fig)
    fax = frac_fig.add_subplot(111)

    fprime_fig = Figure(dims)
    FigureCanvas(fprime_fig)
    fpax = fprime_fig.add_subplot(111)

    diff_fig = Figure(dims)
    FigureCanvas(diff_fig)
    dax = diff_fig.add_subplot(111)

    psmooth_fig = Figure(dims)
    FigureCanvas(psmooth_fig)
    smoothax = psmooth_fig.add_subplot(111)

    spec_fig = Figure(dims)
    FigureCanvas(spec_fig)
    sax = spec_fig.add_subplot(111)

    # make the plots
    pt = np.linspace(20, 200, 200)
    for c in [1.0, 0.98, 0.95]:
        spec = psmooth(pt, c=c) * np.exp(-psmooth(pt, c=c) / 30)
        fax.plot(pt, frac(pt, c=c), label=f'{c}')
        fpax.plot(pt, fprime(pt, c=c), label=f'{c}')
        dax.plot(pt, diff(pt, c=c), label=f'{c}')
        sax.plot(pt, spec * diff(pt, c=c), label=f'{c}')
        smoothax.plot(pt, psmooth(pt, c=c), label=f'{c}')
    dress(fax, r'$p_{\rm T} / p_{\rm T}^{\rm s}$')
    dress(fpax)
    dress(dax, r'$dp_{\rm T}^{\rm s} / dp_{\rm T}$')
    dress(sax, r'$dN / dp_{\rm T}$')
    dress(smoothax)
    if not os.path.isdir(plots):
        os.mkdir(plots)
    opts = dict(bbox_inches='tight')
    frac_fig.savefig(f'{plots}/fracs.pdf', **opts)
    fprime_fig.savefig(f'{plots}/fprime.pdf', **opts)
    diff_fig.savefig(f'{plots}/diff.pdf', **opts)
    spec_fig.savefig(f'{plots}/spec.pdf', **opts)
    psmooth_fig.savefig(f'{plots}/ptsmooth.pdf', **opts)

if __name__ == '__main__':
    make_plots()
