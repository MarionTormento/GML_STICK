# INVERTED MEMORY V3.0
# ____________________
# Improved version of an inverted memory network following STICK using Neuron and Synapses class. 
# Potentially easily scalable
# input: input spike and recall spike
# output: spiking time for each neuron, and comparison to the expected value
# 
# Written by : Marion Tormento
# July 2018
# ____________________

from computation import *

# Initialisation
# Create the neurons       
inpt = Neuron('input')
first = Neuron('first')
last = Neuron('last')
acc = Neuron('acc')
recall = Neuron('recall')
output = Neuron('output')
inputNeuron = [inpt, recall]
otherNeuron = [first, last, acc, output]

# Update the spike and synapses for each neuron
inpt.spikeTime = [0,  45.02]
inpt.updateSyn([['V', first, we, Tsyn], ['V', last, 0.5*we, Tsyn]])
recall.spikeTime = [100]
recall.updateSyn([['ge', acc, wacc/100, Tsyn], ['V', output,we, 2*Tsyn+Tneu]])
first.updateSyn([['V', first, wi, Tsyn], ['ge', acc, wacc/100, Tsyn+Tmin]])
last.updateSyn([['ge', acc, -wacc/100, Tsyn]])
acc.updateSyn([['V', output, we, Tsyn]])

# Init and compute the network
invertedMemory = Network("Inverted Memory", inputNeuron, otherNeuron)
invertedMemory = computation(invertedMemory)
