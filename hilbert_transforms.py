#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hilbert Transform

This python code for decomposing a whisking bout into phase, amplitude, and offset using the Hilbert Transform is based on the Matlab code developed in the Neurophysics Lab at UCSD. 

@author: Marie Tolkiehn, University of Bristol (2020)
"""

import numpy as np

def phase_from_hilbert( signal, Fs, bp= [6,30] ):
    """ Computationally, the Hilbert Transform is the Fourier
    % Transform with zero amplitude at all negative frequencies.  This
    % is equivalent to phase-shifting the time-domain signal by 90 degrees
    % at all frequencies and then adding this as an imaginary signal to the 
    % original signal.
    % So for example, the signal cos(t) becomes cos(t) + i sin(t).  
    %
    %The phase of the original signal is taken as the angle of this new
    %complex signal.
    %
    %inputs -  
    %    signal - vector containing whisker angle
    %    Fs   - sampling rate (Hz)
    %    bp   - frequency range for band-pass filtering, defaults= [6, 30] as 
    %           used in Chen, S., Augustine, G. J., & Chadderton, P. (2016)
    %
    %outputs - 
    %    phase  - phase estimate from Hilbert transform
    %    filtered_signal - input signal after filtering 
    """
    # de-trend the signal with a band-pass filter
    from scipy.signal import buttord, butter, filtfilt
    #scipy.signal.buttord(wp, ws, gpass, gstop, analog=False)

    bp = np.array(bp) * 2 / Fs # convert Hz to radians/S
    [N, Wn] = buttord( bp, bp * [.5, 1.5], 3, 20) 
    [B,A] = butter(N,Wn, btype='bandpass')
    
    # zero-phase filtering, emulate matlab's behaviour with odd padding
    filtered_sig = filtfilt(B,A,signal,padtype = 'odd', padlen=3*(max(len(B),len(A))-1)) 

    # remove negative frequency component of Fourier transform
    X = np.fft.fft(filtered_sig)
    halfway = int(1 + np.ceil(len(X)/2))
    X[halfway:] = 0 ;
    ht_signal = np.fft.ifft(X);

    # return phase
    phase = np.angle(ht_signal)
    return phase, filtered_sig



def get_slow_var(sig, p, operation):
    """ Use the phase (p) to find the turning points of the whisks (tops and
    bottoms), and calculate a value on each consecutive whisk using the
    function handle (operation).  The values are calculated twice per
    whisk cycle using both bottom-to-bottom and top-to-top.  The values
    are linearly interpolated between whisks.
    
    Python code for decomposing a whisking bout into phase, amplitude, and
    offset using the Hilbert Transform.
    
    This code was based on code developed by the Neurophysics Lab at UCSD.
    
    Primary motor cortex reports efferent control of vibrissa motion on
    multiple timescales DN Hill, JC Curtis, JD Moore, D Kleinfeld - Neuron,
    2011"""
    # Find crossings
    tops = (p[0:-1]<0) & (p[1:]>=0)
    bottoms = (p[:-1]>=np.pi/2) & (p[1:]<=-np.pi/2)
    out = np.zeros( (len(sig),) )

    temp = []
    pos = []
    inx = [i for i, x in enumerate(tops) if x]
    for j in range(1,len(inx)):
        vals = sig[ inx[j-1]:inx[j]]
        temp.append(operation(vals))

    if len(inx)>1:
        pos = np.round(inx[0:-1] + np.diff(inx)/2)

    inxb = [i for i, x in enumerate(bottoms) if x]
    for j in range(1,len(inxb)):
        vals = sig[inxb[j-1]:inxb[j]]
        temp.append(operation(vals))

    if len(inxb)>1:
        pos = np.append(pos, np.round(inxb[:-1] + np.diff(inxb)/2))
    
    # Sort
    i = np.argsort(pos)
    posa = pos[i] #reorder
    pos = np.concatenate([np.array([0]),posa,[len(sig)]])

    if not temp:
        temp = operation(sig) * [1, 1]
    else:
        temp = np.array(temp)
        temp = np.concatenate([[temp[i[0]]], temp[i], [temp[i[-1]]]])

    # make piecewise linear signal
    for j in np.arange(1,len(pos)):
        ins = np.arange(int(pos[j-1]), int(pos[j]))
        out[ins] = np.linspace(temp[j-1], temp[j], len(ins))
        
    return out, tops, bottoms
