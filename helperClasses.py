import constants as C
import random
import math

### ClockManager ###

class ClockManager(object):
    

    def __init__(self, evntTimeGen, queue):

        self.queue = queue
        self.evntTimeGen = evntTimeGen
        self.clocks = self.initClocks()
        self.time = 0
        self.prevTime = None



    def updateClocks(self, event):
        
        eventType = event[C.EVENT_TYPE]
        t  = event[C.EVENT_TIME]
        
        if eventType == C.SERVICE: #Customer is served

            if self.queue.state > 0: #Queue non-empty

                self.clocks[C.ARRIVAL] += -t
                self.clocks[C.SERVICE] = self.evntTimeGen.scheduleService()

            else: # Queue is now empty

                self.clocks[C.ARRIVAL] += -t
                self.clocks[C.SERVICE] = float('inf')

        else: # Customer arrives
            
            self.clocks[C.ARRIVAL] = self.evntTimeGen.scheduleArrival()

            wasEmpty = self.queue.prevState == 0
            if wasEmpty:
                
                self.clocks[C.SERVICE] = self.evntTimeGen.scheduleService()

            else:
                
                self.clocks[C.SERVICE] += -t

        self.prevTime = self.time
        self.time += t



    def initClocks(self):

        clocks = [None]*2
        clocks[C.ARRIVAL] = self.evntTimeGen.scheduleArrival()
        clocks[C.SERVICE] = float('inf')

        return clocks

    
    def reset(self):

        self.clocks = self.initClocks()
        self.time = 0
        self.prevTime = None       
    

### EventTimeGenerator ###

class EventTimeGenerator(object):

    def __init__(self, arrivalDist, params):

        self.arrivalDist = arrivalDist
        self.params = params
        self.switch = self.buildSwitch()
        usesNormal = arrivalDist in (C.AUTO_CORR_A, C.AUTO_CORR_B)
        self.normalGen = NormalGenerator() if usesNormal else None


    def buildSwitch(self):

        switch = dict()

        switch[C.EXPONENTIAL] = self.exponential
        switch[C.WEIBULL] = self.weibull
        switch[C.AUTO_CORR_A] = self.autoCorrA
        switch[C.AUTO_CORR_B] = self.autoCorrB
        
        return switch


    
    def scheduleService(self): 

        a = .99
        (U, V) = (random.random(), random.random())
        
        return a*(U+V)

        
    
    def scheduleArrival(self):

        return self.switch[self.arrivalDist]()
    


    def exponential(self):

        lmbda = self.params[C.LAMBDA]
        U = random.random()
        return -math.log(U)/lmbda

    def weibull(self):

        alpha = self.params[C.ALPHA]
        lmbda = self.params[C.LAMBDA]
        U = random.random()
        return ((-math.log(U))**(1/alpha))/lmbda

    def autoCorrA(self):
        
        c = 1/math.sqrt(2)
        Y = c*(self.normalGen.getNext() - self.normalGen.getPrev())
        X = -math.log(self.normCDF(Y))
        return X

    def autoCorrB(self):
        
        c = 1/math.sqrt(2)
        Y = c*(self.normalGen.getNext() + self.normalGen.getPrev())
        X = -math.log(self.normCDF(Y))
        return X
    
    def normCDF(self, x):

        flip = x < 0
        x = -x if flip else x

        a1 = 0.4361836
        a2 = -0.1201676
        a3 = 0.9372980
        y = 1/(1+0.33267*x)
        
        v = 1 - ( 1/(math.sqrt(2*math.pi)) )*( a1*y+a2*(y**2)+a3*(y**3) )*math.exp(-((x**2)/2))
        if flip:
            v = 1 - v

        return v


### Normal Generator ###

class NormalGenerator(object):

    def __init__(self):

        self.current = 0
        self.last = self.genZ()[1]
        self.bufferSize = 1000
        self.buffer = self.rebuffer()

    def rebuffer(self):

        buffer = [None]*self.bufferSize
        
        for i in range(int(self.bufferSize/2)):

            (Z1, Z2) = self.genZ()
            buffer[2*i] = Z1
            buffer[2*i+1] = Z2
        
        return buffer
    
    def genZ(self):

            (U, V) = (random.random(), random.random())
            Z1 = (-2*math.log(U))**(1/2)*math.cos(2*math.pi*V)
            Z2 = (-2*math.log(U))**(1/2)*math.sin(2*math.pi*V)
            return (Z1, Z2)     

    def getNext(self):

        if self.current >= self.bufferSize:
          
            self.last = self.buffer[self.current-1]
            self.buffer = self.rebuffer()
            self.current = 0

        Z = self.buffer[self.current]
        self.current += 1
        return Z
            

    def getPrev(self):

        if self.current == 0:
            return self.last
        
        return self.buffer[self.current-1]
        
    
    

    
    
    
        
        




