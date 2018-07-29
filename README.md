# GML_STICK
Personal implementation of STICK following the method presented in the following paper https://arxiv.org/abs/1507.06222

# What's in the box?

invertedmemory_v2.py: implementation of the inverted memory network using two classes: neuron and synapses. Each neuron have N synapses representing each of its synaptic connection and containing the following characteristics: post-synaptic neuron, type of synapses, weight and time constant. After a first initialisation which allows us to describe the neural network, and to fill the input and recall spiking time, the computation process is launched. The process is split between the input neurons and the other neurons (internal and output). The first part, for the input, looks for the spiking time of the inputs to launch the dynamics of the connected neurons. The second part looks for the "actionTime" of each neuron, to activate the synaptic connections and update the potential. If the potential of the neuron reaches the spiking threshold Vt, the synaptic dynamic of the neuron is activated. Once the output neurons has spiked twice, and hence received the wanted information the process is exited thanks to a break command. Once the process is done, the results are printed: for each neuron, its spiking time are given, and the dTout expected and obtained are compared.

memory_v2.py: similar code for the memory network.

old versions folder: previous versions of the memory and inverted memory networks, using only a neuron class (kept for personal information).

# Next improvements
The version 2.0 highlights a framework (init, computation, results) that could be copied easily for each network that does not have gf-synapses (as the dynamics for now only accounts for V and ge-synapses). A soon improvement will be to separate the computation process and common constant in a separate file that can be called by each network file (where only the init, and results would be explicitely written). With this configuration, other types of network can be easily tested (min, max, substractor, ...). The computation process can still be improved by replacing the for loop by a while loop (avoids the case where the computation is longer than compTime).

A next version would account for each type of synapses (in particular gf-synapses). 

Finally, it has been noted that some values of t_in^2 create hysteresis during the computation that hence return wrong values for dTout. This phenomenon should be investigated 