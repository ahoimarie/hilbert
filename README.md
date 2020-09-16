[![Build Status](https://travis-ci.com/ahoimarie/hilbert.svg?token=USnpr24bQjvx6pPPWuJG&branch=master)](https://travis-ci.com/ahoimarie/hilbert)

# Hilbert transform for whisker analysis

This python code for decomposing a whisking bout into phase, amplitude, and offset using the Hilbert Transform is based on the Matlab code developed in the Neurophysics Lab at UCSD.

> Primary motor cortex reports efferent control of vibrissa motion on multiple timescales DN Hill, JC Curtis, JD Moore, D Kleinfeld - Neuron, 2011

Please also see [Dan Hills GitHub repo](https://github.com/danamics/HilbertTransform) for further information.

Computationally, the Hilbert Transform is the Fourier Transform with zero amplitude at all negative frequencies.  This is equivalent to phase-shifting the time-domain signal by 90 degrees at all frequencies and then adding this as an imaginary signal to the original signal.
So for example, the signal cos(t) becomes cos(t) + i sin(t).

The phase of the original signal is taken as the angle of this new complex signal.

*inputs*
* signal  - vector containing whisker angle
* Fs   - sampling rate (Hz)
* bp - frequency range for band-pass filtering

*outputs*.
* phase  - phase estimate from Hilbert transform
* filtered_signal - input signal after filtering


