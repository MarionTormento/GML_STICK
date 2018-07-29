# MEMORY V1.0
# ____________________
# First draft of a memory network following STICK
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
compTime = 50000

class Neuron():
    """docstring for Neuron"""
    def __init__(self):
        super(Neuron, self).__init__()
        self.V = 0
        self.updateRule = []
        self.spikeTime = []
        self.actionTime = []

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
     
# Initialisation   
inpt = Neuron()
inpt.spikeTime = [0, 30]
recall = Neuron()
recall.spikeTime = [150]
first = Neuron()
last = Neuron()
acc = Neuron()
acc2 = Neuron()
ready = Neuron()
output = Neuron()

# Computation 
for t in range(50000): # t in 10us chunk
    # input
    if t == 100*inpt.spikeTime[0] or t == 100*inpt.spikeTime[1]:
        # first
        first.time(t, Tsyn)
        first.voltage(we)
        # last
        last.time(t, Tsyn)
        last.voltage(0.5*we)

    # recall
    if t == 100*recall.spikeTime[0]:
        # output
        output.time(t, Tsyn)
        output.voltage(we)
        # acc
        acc2.time(t, Tsyn)
        acc2.voltage(wacc/100)

    # first
    try:
        if t == first.actionTime[0]:
            # own dynamics
            first.updateAction(t)
            first.V += first.updateRule[0]

            if first.V >= Vt:
                # Neuron spiking and reset
                first.spike(t)
                first.V = Vreset
                # inhibition
                first.time(100*first.spikeTime[-1], Tneu + Tsyn)
                first.voltage(wi/100)
                # acc
                acc.time(100*first.spikeTime[-1], Tsyn)
                acc.voltage(wacc/100)

            # V-synapses
            del first.updateRule[0], first.actionTime[0]    

    except IndexError:
        pass

    # last
    try:
        if t == last.actionTime[0]:
            # own dynamics
            last.updateAction(t)
            last.V += last.updateRule[0]

            if last.V >= Vt:
                # Neuron spiking, and reset
                last.spike(t)
                last.V = Vreset
                 # acc
                acc2.time(100*last.spikeTime[-1], Tsyn)
                acc2.voltage(wacc/100)

            # V-synapses
            del last.updateRule[0], last.actionTime[0]

    except IndexError:
        pass

    # acc
    try:
        if t >= acc.actionTime[0]:
            # own dynamics
            acc.updateAction(t)
            acc.V += acc.updateRule[0]

            if acc.V >= Vt:
                # Neuron spiking
                acc.spike(t)
                # acc2
                acc2.time(100*acc.spikeTime[-1], Tsyn)
                acc2.voltage(-wacc/100)
                # ready
                ready.time(100*acc.spikeTime[-1], Tsyn)
                ready.voltage(we)
                # reset
                acc.V = Vreset
                del acc.updateRule[0], acc.actionTime[0]

    except IndexError:
        pass
            

    # acc2
    try:
        if t >= acc2.actionTime[0]:
            # own dynamics
            acc2.updateAction(t)
            acc2.V += acc2.updateRule[0]
            # print(t, acc2.V, acc2.actionTime)
            if acc2.V >= Vt:
                # Neuron spiking
                acc2.spike(t)
                # output
                output.time(100*acc2.spikeTime[-1], Tsyn)
                output.voltage(we)
                # reset
                acc2.V = Vreset
                del acc2.updateRule[0], acc2.actionTime[0]

    except IndexError:
        pass

   # ready
    try:
        if t >= ready.actionTime[0]:
            # own dynamics
            ready.updateAction(t)
            ready.V += ready.updateRule[0]

            if ready.V >= Vt:
                # neuron spiking
                ready.spike(t)
                ready.V = Vreset
            
            del ready.updateRule[0], ready.actionTime[0]
    except IndexError:
        pass
    # output
    try:
        if t >= output.actionTime[0]:
            # own dynamics
            output.updateAction(t)
            output.V += output.updateRule[0]

            if output.V >= Vt:
                # neuron spiking
                output.spike(t)
                output.V = Vreset

            # V-synapses
            del output.updateRule[0], output.actionTime[0]
            # Break the for-loop is both output has spiked twice
            if len(output.spikeTime) == 2:
                break

    except IndexError:
        pass

# Results
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

