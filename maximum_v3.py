# MAXIMUM V3.0
# ____________________
# Maximum network following STICK using Neuron and Synapses class. 
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
larger1 = Neuron('smaller1')
larger2 = Neuron('smaller2')
output = Neuron('output')
inputNeuron = [inpt1, inpt2]
otherNeuron = [larger1, larger2, output]

# Update the spike and synapses for each neuron
inpt1.spikeTime = [0, 23.5]
inpt1.updateSyn([['V', larger2, 0.5*we, Tsyn], ['V', output, 0.5*we, Tsyn]])
inpt2.spikeTime = [0, 35.4]
inpt2.updateSyn([['V', larger1, 0.5*we, Tsyn], ['V', output, 0.5*we, Tsyn]])
larger1.updateSyn([['V', larger2, wi, Tsyn]])
larger2.updateSyn([['V', larger1, wi, Tsyn]])

# Init and compute the network
maximum = Network("Maximum", inputNeuron, otherNeuron)
maximum = computation(maximum)
