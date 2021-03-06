# GML_STICK
Personal implementation of STICK following the method presented in the following paper https://arxiv.org/abs/1507.06222

# What's in the box ? V_3.0
computation.py : "header" file containing the constants, the computation loop and the function to print the results and figures (network, chronogram).

each "network".py file only contains the initialisation of the neurons, synapses and network. The network is then fed to the computation function that outputs the spike time of each neuron, and a comparison of the dTout expected and obtained.

# What's in the box? _ V2.0

invertedmemory_v2.py: implementation of the inverted memory network using two classes: neuron and synapses. Each neuron have N synapses representing each of its synaptic connection and containing the following characteristics: post-synaptic neuron, type of synapses, weight and time constant. After a first initialisation which allows us to describe the neural network, and to fill the input and recall spiking time, the computation process is launched. The process is split between the input neurons and the other neurons (internal and output). The first part, dediated to the input, looks for the spiking time of the neuron to update the action time, and the update rule of the post-synaptic neurons. The second part looks for the action time of each neuron to "activate" the synaptic connections and update the potential. If the potential of the neuron reaches the spiking threshold Vt, the neuron spikes and reset to Vreset and its post-synaptic neurons are updated similarly than for the input neurons. Once the output neurons has spiked twice, and hence received the wanted information, the process is exited thanks to a break command. Once the process is done, the results are printed: for each neuron, its spiking time are given, and the dTout expected and obtained are compared.

memory_v2.py: similar code for the memory network.

old versions folder: previous versions of the memory and inverted memory networks, using only a neuron class (kept for personal information).

# Useful vocabulary and information
The for loop used in the computation is updated with a step of 10us corresponding to the smallest time scale of the neuron (Tneu). Thus, compTime is in us.

Class Neuron():

        self.name = name 		# Name of the neuron
        self.V = 0				# Potential of the neuron at t
        self.spikeTime = []		# List of spiking time of the neuron
        self.actionTime = []	# List of instant t_i where the neuron potential should be updated
        self.updateRule = []	# List of dV_i to update the neuron potential from action time t_i to t_{i+1}
        self.nbSynapses = 0		# Number of Synaptic connection
        self.synapses = []		# List of Synapses
        self.isVsynapes = 0		# Special rule in case the synapse is a V-synapses 

class Synapses():

        self.type = syn  		# Type of synapses (V/ge/gf)
        self.post = neuron 		# Post-synaptic neuron
        self.W = weight 		# weight of the synapses
        self.T = time    		# time constant

# Next improvements
The version 2.0 highlights a framework (init, computation, results) that could be copied easily for each network that does not have gf-synapses (as the dynamics for now only accounts for V and ge-synapses). An improvement to come soon will be to separate the computation process and common constant in a separate file that can be called by each network file (where only the init, and results would be explicitely written).  The computation process can still be improved by replacing the for loop by a while loop (avoids the case where the computation is longer than compTime). => DONE IN V3.0

With this configuration, other types of network can be easily tested (min, max, substractor, ...). => DONE IN V3.0

A next version would account for each type of synapses (in particular gf-synapses). 

Finally, the way network are created could be improved so that composition between different network could be achieved (for exemple, the linear combination network is composed of the memory and substractor network)