# MAXIMUM V3.0
# ____________________
# Simple Substractor network following STICK using Neuron and Synapses class. 
# input: network containing input spike and recall spike
# output: spiking time for each neuron, and comparison to the expected value
# 
# Written by : Marion Tormento
# July 2018
# ____________________

from computation import *

# Initialisation
# Create the neurons        
inpt1 = Neuron('input1')
inpt2 = Neuron('input2')
sync1 = Neuron('sync1')
sync2 = Neuron('sync2')
inb1 = Neuron('inb1')
inb2 = Neuron('inb2')
outputpl = Neuron('output+')
outputmin = Neuron('output-')
inputNeuron = [inpt1, inpt2]
otherNeuron = [sync1, sync2, inb1, inb2, outputpl, outputmin]

# Update the spike and synapses for each neuron
inpt1.spikeTime = [0,33]
inpt1.updateSyn([['V', sync1, 0.5*we, Tsyn]])
inpt2.spikeTime = [0, 18]
inpt2.updateSyn([['V', sync2, 0.5*we, Tsyn]])
sync1.updateSyn([['V', inb1, we, Tsyn],['V', inb2, wi, Tsyn],['V', outputpl, we, Tmin+3*Tsyn+2*Tneu],['V', outputmin, we, 3*Tsyn+2*Tneu]])
sync2.updateSyn([['V', inb1, wi, Tsyn],['V', inb2, we, Tsyn],['V', outputmin, we, Tmin+3*Tsyn+2*Tneu],['V', outputpl, we, 3*Tsyn+2*Tneu]])
inb1.updateSyn([['V', outputpl, 2*wi, Tsyn]])
inb2.updateSyn([['V', outputmin, 2*wi, Tsyn]])
outputpl.updateSyn([['V', inb2, 0.5*we, Tsyn]])
outputmin.updateSyn([['V', inb1, 0.5*we, Tsyn]])

# Init and compute the network
sub_simple = Network("Subtractor simple", inputNeuron, otherNeuron)
sub_simple = computation(sub_simple)
