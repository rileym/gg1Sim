import constants as C
import GG1queue
import sys
import time

N = 26000
termTime = 1000



def main():

    tStart = time.time()
    
    lmbda = 1
    expMus = 0
    qExp = GG1queue.Queue(C.EXPONENTIAL, [lmbda], termTime)
    
    lmbda = 0.8856899
    alpha = 2.1013491
    params = [None]*2
    params[C.ALPHA] = alpha
    params[C.LAMBDA] = lmbda
    weibAMus = 0
    qWeibA = GG1queue.Queue(C.WEIBULL, params, termTime)
    
    
    lmbda = 1.7383757
    alpha = 0.5426926
    params = [None]*2
    params[C.ALPHA] = alpha
    params[C.LAMBDA] = lmbda
    weibBMus = 0
    qWeibB = GG1queue.Queue(C.WEIBULL, params, termTime)

    acAMus = 0
    qAutoCorrA = GG1queue.Queue(C.AUTO_CORR_A, None, termTime)
    
    acBMus = 0
    qAutoCorrB = GG1queue.Queue(C.AUTO_CORR_B, None, termTime)
    
    
    for i in range(N):
        
        expMus += qExp.simulate()
        qExp.reset()
        
        weibAMus += qWeibA.simulate()
        qWeibA.reset()

        weibBMus += qWeibB.simulate()
        qWeibB.reset()

        acAMus += qAutoCorrA.simulate()
        qAutoCorrA.reset()

        acBMus += qAutoCorrB.simulate()
        qAutoCorrB.reset()

    f = open('queueOutput.txt', 'w')    

    f.write('\nIterations: ' +str(N) + '\n')
    f.write('Total Time: ' + '{0:.2f}'.format((time.time() - tStart)) + ' seconds\n\n')
    f.write('--------------------  Results  --------------------\n')
    f.write('--------- PART A: Poisson Arrival Process --------- \n\n')
    f.write('L estimate = '+ '{0:.2f}'.format(expMus/N)+'\n\n')
    f.write('--------- PART B: Weibull Arrivals --------- \n\n')
    f.write('L estimate = '+ '{0:.2f}'.format(weibAMus/N)+'\n\n')
    f.write('--------- PART C: Weibull Arrivals --------- \n\n')
    f.write('L estimate = '+ '{0:.2f}'.format(weibBMus/N)+'\n\n')
    f.write('--------- PART D.i: Auto-Correlated Arrivals ---------\n\n')
    f.write('L estimate = ' + '{0:.2f}'.format(acAMus/N) + '\n\n')
    f.write('--------- PART D.ii: Auto-Correlated Arrivals ---------\n\n')
    f.write('L estimate = ' + '{0:.2f}'.format(acBMus/N) + '\n\n')
          
    f.close()

if __name__ == "__main__":
    main()
