# COMPUTATION CODE
# ____________________
# Definition of the different constant, classes and computation loop
# 
# Written by : Marion Tormento
# July 2018
# ____________________

# Constant
Vt = 10 #mV
Vreset = 0 #mV
taum = 100 #ms (100s ? Erreur dans le texte)
tauf = 20 #ms
Tsyn = 1 #ms
Tneu = 0.01 #ms (10us)
Tmin = 10 #ms
Tcod = 100 #ms
Tmax = Tmin + Tcod
wacc = Vt*taum/Tmax
waccb = Vt*taum/Tcod
ge = wacc
we = Vt*taum
wi = -we
dt = 1

class Network():
    def __init__(self, name, Neuron1, Neuron2):
        super(Network, self).__init__()
        self.name = name
        self.input = Neuron1
        self.other = Neuron2

class Neuron():
    def __init__(self, name):
        super(Neuron, self).__init__()
        self.name = name
        self.V = 0
        self.updateRule = []
        self.spikeTime = []
        self.actionTime = []
        self.nbSynapses = 0
        self.synapses = []
        self.isVsynapes = 0

    def voltage(self, w):
        self.updateRule.append(dt*(w/taum))

    def updateAction(self, time):
        if len(self.actionTime) < 2:
            pass
        else:
            if time >= self.actionTime[1]:
                self.updateRule[0] += self.updateRule[1]
                del self.updateRule[1], self.actionTime[0]

    def time(self, instant, timeCste):
        val = round(instant + 100*timeCste, 0)
        self.actionTime.append(val)

    def spike(self, instant):
        # val = int(instant + 100*Tneu)/100
        val = round(instant/100 + Tneu, 2)
        self.spikeTime.append(val)

    def updateSyn(self, syn):
        self.nbSynapses = len(syn)
        for post in syn:
            self.synapses.append(Synapses(post[0], post[1], post[2], post[3]))

class Synapses():
    def __init__(self, syn, neuron, weight, time):
        super(Synapses, self).__init__()
        self.type = syn
        self.post = neuron
        self.W = weight
        self.T = time


# Computation

def computation(network):
    inputNeuron = network.input
    otherNeuron = network.other
    computationComplete = False
    t = 0
    while computationComplete == False:
        for neuron in inputNeuron:
            for spike in neuron.spikeTime:
                spike = 100*spike
                if t == spike:
                    neuron.V += Vt
                    if neuron.V >= Vt:
                        neuron.V = Vreset
                        for synapses in neuron.synapses:
                            synapses.post.time(t, synapses.T)
                            synapses.post.voltage(synapses.W)
                            if synapses.type == 'V':
                                synapses.post.isVsynapes = 1
                            else:
                                synapses.post.isVsynapes = 0
                else:
                    try:
                        if t >= neuron.actionTime[0]:
                            neuron.updateAction(t)
                            neuron.V += neuron.updateRule[0]
                            if neuron.V >= Vt:
                                neuron.V = Vreset
                                for synapses in neuron.synapses:
                                    synapses.post.time(t, synapses.T)
                                    synapses.post.voltage(synapses.W)
                                    if synapses.type == 'V':
                                        synapses.post.isVsynapes = 1
                                    else:
                                        synapses.post.isVsynapes = 0  

                            if neuron.isVsynapes == 1: # meaning its a V synapses
                                del neuron.updateRule[0], neuron.actionTime[0]
                    except IndexError:
                        pass

        for neuron in otherNeuron:
            try:
                if t >= neuron.actionTime[0]:
                    neuron.updateAction(t)
                    neuron.V += neuron.updateRule[0]
                    if neuron.V >= Vt:
                        # Neuron spiking and reset
                        neuron.spike(t)
                        neuron.V = Vreset

                        # Update the postsynaptic neuron
                        for synapses in neuron.synapses:
                            synapses.post.time(100*neuron.spikeTime[-1], synapses.T)
                            synapses.post.voltage(synapses.W)
                            if synapses.type == 'V':
                                synapses.post.isVsynapes = 1
                            else:
                                synapses.post.isVsynapes = 0
                        # reset the neuron completely
                        if neuron.isVsynapes == 0:
                            del neuron.updateRule[0], neuron.actionTime[0]

                    if neuron.isVsynapes == 1: # meaning its a V synapses
                        del neuron.updateRule[0], neuron.actionTime[0]

                    if neuron.name == 'output' and len(neuron.spikeTime) == 2:
                        print("Computation lasted for ", neuron.spikeTime[-1], "ms")
                        computationComplete = True
                        
            except IndexError:
                pass
        t += 1

    network.input = inputNeuron
    network.other = otherNeuron
    printResults(network)
    return network

def printResults(network):
    print(network.name)
    print("Spike time for each neuron")
    for neuron in network.input:
        print(neuron.name,": ", neuron.spikeTime)
    for neuron in network.other:
        print(neuron.name, ": ", neuron.spikeTime)
    expectedResult = 0
    if network.name == "Inverted Memory":
        expectedResult = round(Tmax-(network.input[0].spikeTime[1]-network.input[0].spikeTime[0]-Tmin),2)
    elif network.name == "Memory":
        expectedResult = round(network.input[0].spikeTime[1]-network.input[0].spikeTime[0],2)
    elif network.name == "Minimum":
        expectedResult = round(min(network.input[0].spikeTime[1]-network.input[0].spikeTime[0], network.input[1].spikeTime[1]-network.input[1].spikeTime[0]),2)
    elif network.name == "Maximum":
        expectedResult = round(max(network.input[0].spikeTime[1]-network.input[0].spikeTime[0], network.input[1].spikeTime[1]-network.input[1].spikeTime[0]),2)
    obtainedResult = round(network.other[-1].spikeTime[1]-network.other[-1].spikeTime[0],2)
    print("DTout - Result expected:", expectedResult, " / Result obtained with the network: ", obtainedResult)
    print("Error: ", round((expectedResult - obtainedResult)/expectedResult*100,2) )