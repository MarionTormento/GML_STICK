# MEMORY V3.0
# ____________________
# Improved version of a memory network following STICK using Neuron and Synapses class. 
# input: network containing input spike and recall spike
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
acc2 = Neuron('acc2')
recall = Neuron('recall')
ready = Neuron('ready')
output = Neuron('output')
inputNeuron = [inpt, recall]
otherNeuron = [first, last, acc, acc2, ready, output]

# Update the spike and synapses for each neuron
inpt.spikeTime = [0, 98.1]
inpt.updateSyn([['V', first, we, Tsyn], ['V', last, 0.5*we, Tsyn]])
recall.spikeTime = [150]
recall.updateSyn([['ge', acc2, wacc/100, Tsyn], ['V', output, we, Tsyn]])
first.updateSyn([['V', first, wi, Tsyn], ['ge', acc, wacc/100, Tsyn]])
last.updateSyn([['ge', acc2, wacc/100, Tsyn]])
acc.updateSyn([['V', ready, we, Tsyn], ['ge', acc2, -wacc/100, Tsyn]])
acc2.updateSyn([['V', output, we, Tsyn]])

# Init and compute the network
memory = Network("Memory", inputNeuron, otherNeuron)
memory = computation(memory)
