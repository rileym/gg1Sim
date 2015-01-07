import constants as C
import helperClasses


class Queue(object):

    def __init__(self, arrivalDist, params, terminalTime):

        self.terminalTime = terminalTime
        arvlGen = helperClasses.EventTimeGenerator(arrivalDist, params)
        self.clockMngr = helperClasses.ClockManager(arvlGen, self)
        self.state = 0
        self.prevState = None
        self.runningIntegral = 0



    def step(self):

        event = self.getEvent()
        t = event[C.EVENT_TIME]
        self.updateState(event)
        self.clockMngr.updateClocks(event)
        
        isOver = self.clockMngr.time >= self.terminalTime
        if not isOver:
            
            self.runningIntegral += self.prevState*t
            
        else:
            
            truncEventTime = self.terminalTime - self.clockMngr.prevTime
            self.runningIntegral += self.prevState*truncEventTime

        return isOver


        
    def updateState(self, event):

        self.prevState = self.state
        arrival = event[C.EVENT_TYPE] == C.ARRIVAL
        self.state += 1 if arrival else -1



    def getEvent(self):

        clocks = self.clockMngr.clocks
        t = min(clocks)
        eType = clocks.index(t)

        event = [None]*2
        event[C.EVENT_TYPE] = eType
        event[C.EVENT_TIME] = t

        return event


    
    def simulate(self):

        while not self.step():
            pass

        return self.runningIntegral/self.terminalTime

        

    def reset(self):

        self.clockMngr.reset()
        self.state = 0
        self.prevState = None
        self.runningIntegral = 0
    

    
        
