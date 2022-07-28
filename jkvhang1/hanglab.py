# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import wave
import numpy
import matplotlib.pyplot as plt

SAMPLE_RATE = 44100
NYQUIST_RATE = SAMPLE_RATE / 2

def time(w, rate=SAMPLE_RATE):
    """Return the time values belonging to samples"""
    
    return numpy.linspace(0, w.shape[1], w.shape[1]) / rate
    
def freq(spec, rate=SAMPLE_RATE):
    """Return the frequency values belonging to FFT bins"""
    
    return numpy.linspace(0, rate / 2, spec.shape[1])

def readwave(filename):
    """Read a sound sample from a wave file."""
    
    f = wave.open(filename, 'r')
    chan = f.getnchannels()
    rate = f.getframerate()
    fram = f.getnframes()
    bits = f.getsampwidth()
    data = f.readframes(fram)
    
    f.close
    
    if rate != SAMPLE_RATE:
        print("Warning: non-default sampling rate!")
    
    if bits == 2:
        w = numpy.fromstring(data, dtype="<h") / 32768.0
    else:
        raise Exception("Unsupported bit depth, use 16 bit only!")
        
    # reshape stereo signal
    w = w.reshape((int(w.size / chan), chan))
    w = w.transpose()
    
    return w
    
def writewave(filename, w, rate=SAMPLE_RATE):
    """Write a sound sample to a wave file."""  
    
    data = numpy.int16((w.transpose() * 32768.0)).tobytes()
    chan = w.shape[0]
    
    f = wave.open(filename, 'w')
    f.setframerate(rate)
    f.setnchannels(chan)
    f.setsampwidth(2)
    
    f.writeframes(data)
    f.close
    
def subplots(d):
    f, ax = plt.subplots(d.shape[0], sharex=True, sharey=True, squeeze=True)
    
    if d.shape[0] == 1:
        return f, [ax]
    else:
        return f, ax.flatten()
    
def plotwave(w, rate=SAMPLE_RATE, xlim=None):
    t = time(w, rate)    
   
    f, ax = subplots(w)
    for i in range(0, len(ax)):
        ax[i].grid(True)
        if xlim != None:
            ax[i].set_xlim(xlim)
        else:
            ax[i].set_xlim([numpy.min(t), numpy.max(t)])
        ax[i].set_ylim([-1,1])    
        ax[i].grid(True)
        ax[i].plot(t, w[i,:])
        
    ax[-1].set_xlabel('t [sec]')
    
def plotspec(s, rate=SAMPLE_RATE):
    sp = numpy.log10(numpy.abs(s))
    fq = freq(s, rate)
    mmm = numpy.max(sp)
    
    f, ax = subplots(s)
    for i in range(0, len(ax)):
        ax[i].set_xlim([numpy.min(fq), numpy.max(fq)])
        ax[i].set_ylim([0,mmm])   
        ax[i].grid(True)
        ax[i].fill_between(fq, 0, sp[i,:], color='blue')
    
    ax[-1].set_xlabel('f [Hz]')
    
def plotspecgram(w, rate=SAMPLE_RATE, xlim=None):
    nfft = 512
    t = time(w, rate)
    
    f, ax = subplots(w)
    for i in range(0, len(ax)):
        ax[i].specgram(w[i,:], NFFT=nfft, Fs=rate)
        if xlim != None:
            ax[i].set_xlim(xlim)
        else:
            ax[i].set_xlim([numpy.min(t), numpy.max(t)])    
        ax[i].set_ylim([0, rate / 2.0])
        ax[i].set_ylabel('f [Hz]')        

    ax[-1].set_xlabel('t [sec]')
