# MEMORY V2.0
# ____________________
# Improved version of an inverted memory network following STICK using Neuron and Synapses class. 
# Potentially easily scalable
# input: input spike and recall spike
# output: spiking time for each neuron, and comparison to the expected value
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
            if t >= self.actionTime[1]:
                self.updateRule[0] += self.updateRule[1]
                del self.updateRule[1], self.actionTime[0]

    def time(self, instant, timeCste):
        val = int(instant + 100*timeCste)
        self.actionTime.append(val)

    def spike(self, instant):
        val = int(instant + 100*Tneu)/100
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
inpt.spikeTime = [0, 23.1]
inpt.updateSyn([['V', first, we, Tsyn], ['V', last, 0.5*we, Tsyn]])
recall.spikeTime = [150]
recall.updateSyn([['ge', acc2, wacc/100, Tsyn], ['V', output, we, Tsyn]])
first.updateSyn([['V', first, wi, Tsyn], ['ge', acc, wacc/100, Tsyn]])
last.updateSyn([['ge', acc2, wacc/100, Tsyn]])
acc.updateSyn([['V', ready, we, Tsyn], ['ge', acc2, -wacc/100, Tsyn]])
acc2.updateSyn([['V', output, we, Tsyn]])

# Computation
compTime = 50000

for t in range(compTime):
    for neuron in inputNeuron:
        for spike in neuron.spikeTime:
            spike = 100*spike
            if t == spike:
                for synapses in neuron.synapses:
                    synapses.post.time(t, synapses.T)
                    synapses.post.voltage(synapses.W)
                    if synapses.type == 'V':
                        synapses.post.isVsynapes = 1
                    else:
                        synapses.post.isVsynapes = 0
                    # print(t, neuron.name, synapses.post.name, synapses.post.actionTime, synapses.post.updateRule)

    for neuron in otherNeuron:
        try:
            if t >= neuron.actionTime[0]:
                neuron.updateAction(t)
                neuron.V += neuron.updateRule[0]
                if neuron.V >= Vt:
                    # Neuron spiking and reset
                    neuron.spike(t)
                    neuron.V = Vreset

                    if neuron.name == 'acc':
                        print(t, neuron.V, neuron.updateRule, neuron.actionTime)
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
                    break
        except IndexError:
            pass

print("Memory")
print("Spike time for each neuron")
print("input: ", inpt.spikeTime)
print("recall: ", recall.spikeTime)
print("first: ", first.spikeTime)
print("last: ", last.spikeTime)
print("acc: ", acc.spikeTime)
print("acc2: ", acc2.spikeTime)
print("ready: ", ready.spikeTime)
print("output: ", output.spikeTime)
print("DTout: result expected: ", inpt.spikeTime[1]-inpt.spikeTime[0], "/ result obtained: ", output.spikeTime[1]-output.spikeTime[0])

