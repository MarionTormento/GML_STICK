# MINIMUM V3.0
# ____________________
# Minimum network following STICK using Neuron and Synapses class. 
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
smaller1 = Neuron('smaller1')
smaller2 = Neuron('smaller2')
output = Neuron('output')
inputNeuron = [inpt1, inpt2]
otherNeuron = [smaller1, smaller2, output]

# Update the spike and synapses for each neuron
inpt1.spikeTime = [0, 20]
inpt1.updateSyn([['V', smaller1, 0.5*we, Tsyn], ['V', output, 0.5*we, 2*Tsyn+Tneu]])
inpt2.spikeTime = [0, 30]
inpt2.updateSyn([['V', smaller2, 0.5*we, Tsyn], ['V', output, 0.5*we, 2*Tsyn+Tneu]])
smaller1.updateSyn([['V', inpt2, wi, Tsyn], ['V', output, 0.5*we, Tsyn], ['V', smaller2, 0.5*wi, Tsyn]])
smaller2.updateSyn([['V', inpt1, wi, Tsyn], ['V', output, 0.5*we, Tsyn], ['V', smaller1, 0.5*wi, Tsyn]])

# Init and compute the network
minimum = Network("Minimum", inputNeuron, otherNeuron)
minimum = computation(minimum)
