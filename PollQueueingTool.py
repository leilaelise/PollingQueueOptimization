import queueing_tool as qt 
import numpy as np 
from numpy.random import uniform, exponential
from itertools import combinations, permutations, product
import math
import PyQt5.QtWidgets as pyqt
import matplotlib.pyplot as plt
import scipy.signal as signal


#Global variables
precinctPop = 0

def arrival_rate(t):
    #precinctPop = 500   
    if t<=1:
        return 0.156*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=2:
        return 0.087*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=3:
        return 0.095*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=4:
        return 0.112*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=5:
        return 0.087*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=6:
        return 0.054*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=7:
        return 0.072*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=8:
        return 0.067*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=9:
        return 0.063*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=10:
        return 0.067*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=11:
        return 0.068*precinctPop #  np.sin(np.pi*t/2)**2
    elif t<=12:
        return 0.053*precinctPop #  np.sin(np.pi*t/2)**2
    else: 
        return 0.02*precinctPop #-#np.sin(np.pi*t/2)**2
        

    
def arr_f(t):
   # precinctPop = 500
    if t<=1:
        return qt.poisson_random_measure(t,arrival_rate,0.156*precinctPop)
    elif t<=2:
        return qt.poisson_random_measure(t,arrival_rate,0.087*precinctPop)
    elif t<=3:
        return qt.poisson_random_measure(t,arrival_rate,0.095*precinctPop)
    elif t<=4:
        return qt.poisson_random_measure(t,arrival_rate,0.112*precinctPop)
    elif t<=5:
        return qt.poisson_random_measure(t,arrival_rate,0.087*precinctPop)
    elif t<=6:
        return qt.poisson_random_measure(t,arrival_rate,0.054*precinctPop)
    elif t<=7:
        return qt.poisson_random_measure(t,arrival_rate,0.072*precinctPop)
    elif t<=8:
        return qt.poisson_random_measure(t,arrival_rate,0.067*precinctPop)
    elif t<=9:
        return qt.poisson_random_measure(t,arrival_rate,0.063*precinctPop)
    elif t<=10:
        return qt.poisson_random_measure(t,arrival_rate,0.067*precinctPop)
    elif t<=11:
        return qt.poisson_random_measure(t,arrival_rate,0.068*precinctPop)
    elif t<=12:
        return qt.poisson_random_measure(t,arrival_rate,0.053*precinctPop)
    else: 
        return qt.poisson_random_measure(t,arrival_rate,0.02*precinctPop)


def createQueueGraph(num_checkIns,num_pollBooths,checkIn_rate,polling_rate,precinctPop):

    #Create graph adjacent graph nodes 
    adja_list = {0:[1],1:[k for k in range(2,2+num_checkIns)]}
    for k in range(2,2+num_checkIns):
        adja_list.update({k:[l for l in range(2+num_checkIns,2+num_checkIns+num_pollBooths)]})

    #Create graph edges, of type 1, 2, or 3, depending on the type of queue 
    edge_list = {0: {1:1}, 1:{k: 2 for k in range(2, 2+num_checkIns)}}
    for k in range(2,2+num_checkIns):
       edge_list.update({k:{l: 3 for l in range(2+num_checkIns,2+num_checkIns+num_pollBooths)}})
    
    #Generate graph
    g = qt.adjacency2graph(adjacency=adja_list, edge_type=edge_list)

    return g

def createQueueingNetwork(g,checkIn_rate,polling_rate):
    q_classes = {1: qt.QueueServer, 2: qt.QueueServer, 3: qt.QueueServer}
    q_args = {
        1: {
            'arrival_f':arr_f,
            'service_f': lambda t: t,
            'AgentFactory: ': qt.Agent
        },
        2: {
            'service_f': lambda t: t + np.random.exponential(1/checkIn_rate)
        },
        3: {
            'service_f': lambda t: t + np.random.exponential(1/polling_rate)
        }
    }
    
    qn = qt.QueueNetwork(g=g, q_classes=q_classes, q_args=q_args, seed=13)

    return qn

def visualizeGraph(qn,num_checkIns,num_pollBooths):
    qn.g.new_vertex_property('pos')
    pos = {}
    
    #Formatting for graphing
    edge2Value = 0
    edge3Value = 0
    for v in qn.g.nodes(): #For each vertex
        x = 0
        if v==0: #Entering store
            pos[v] = [0, 0]
        elif v==1:
            pos[v] = [0, 0]
        elif v<=(1+num_checkIns):
            if np.mod(v,2)==0:
                x = edge2Value
            else:
                x = -edge2Value
            pos[v] = [x, -1]
            edge2Value += 0.5
        else: #
            if np.mod(v,2)==0:
                x = edge3Value
            else:
                x = -edge3Value
            pos[v] = [x, -2]
            edge3Value += 0.5
    
    qn.g.set_pos(pos)


def SolveQueue(num_checkIns, num_pollBooths, checkIn_rate, polling_rate):    
    #Define polling station parameters: These should be user input
    checkIn_rate = math.ceil(60/checkIn_rate) #people/hr per booth   
    polling_rate = math.ceil(60/polling_rate) #people/hr per booth

    
    g = createQueueGraph(num_checkIns,num_pollBooths,checkIn_rate,polling_rate,precinctPop)
    qn = createQueueingNetwork(g,checkIn_rate,polling_rate)
    visualizeGraph(qn,num_checkIns,num_pollBooths)
   # qn.draw(fname="pollingGraph.png", figsize=(12, 3), bbox_inches='tight')
    
   
    #Run simulation
    qn.initialize(edge_type=1)
    #qn.animate(figsize=(4, 4)) 
    qn.start_collecting_data()
    qn.simulate(t=13)
    
    arrivalData = qn.get_agent_data(edge_type=1)
    prePollData = qn.get_agent_data(edge_type=3)

    lineLengths = []
    lineTimes = []
    feasible = True
    
    for a in range(1,len(prePollData)):
        if (((0,a) in prePollData) == False):
            continue   
         
        lineLength = (arrivalData[(0,a)][0][3] + prePollData[(0,a)][0][3])*6 #in [ft]
        lineTime = (prePollData[(0,a)][0][0] - arrivalData[(0,a)][0][0])
        
        lineLengths.append(lineLength)
        lineTimes.append(lineTime)
        
        if (lineLength > 264):
            feasible = False
        if (lineTime > 0.5):
            feasible = False
    
    #qn.draw(fname="pollingSim.png", figsize=(12, 3), bbox_inches='tight')
    #print(lineTimes)
    return [feasible,lineTimes,qn]

def OrderedPermutations(num_checkIns,num_pollBooths,checkIn_rate,polling_rate):
    weight = polling_rate/checkIn_rate
    
    list1 = np.linspace(1,num_checkIns,num_checkIns)
    list2 = np.linspace(1,num_pollBooths,num_pollBooths)
 
    all_combinations = []


    all_combinations = list(product(list1, list2))

    scoreDict = {}
    for i in range(0,len(all_combinations)):
        combo1 = all_combinations[i]
        combo2 = all_combinations[i]
        score1 = combo1[0]*weight + combo1[1]
        score2 = combo2[0]*weight + combo2[1]
        scoreDict.update({combo1:score1})
        scoreDict.update({combo2:score2})
    

    return sorted(scoreDict)
      
def optimizeQueue(checkIn_rate,polling_rate,cleaning_rate,num_checkIns,num_pollBooths,precinctPop,demographics):

    polling_rate = polling_rate + cleaning_rate
    
    for i in range(0,len(demographics)):
        demographics[i] = (1+demographics[i])*polling_rate
    
    polling_rate = sum(demographics)/len(demographics)
 
    
    resourceOptions = OrderedPermutations(num_checkIns,num_pollBooths,checkIn_rate,polling_rate)   
    
    visited = []
  
    a = 0
    b = len(resourceOptions)-1
    lowestCheckIn = int(resourceOptions[a][0])
    lowestPollBooths = int(resourceOptions[a][1])   
    highestCheckIn = int(resourceOptions[b][0])
    highestPollBooths = int(resourceOptions[b][1])
    visited.append(resourceOptions[a])
    visited.append(resourceOptions[b])
    if(SolveQueue(lowestCheckIn,lowestPollBooths,checkIn_rate,polling_rate)[0]):
        print("Optimal Check-In Stations: ", lowestCheckIn)
        print("Optimal Polling Booths: ",lowestPollBooths)
        lineTimes = SolveQueue(lowestCheckIn,lowestPollBooths,checkIn_rate,polling_rate)[1]
        plotQueue(lineTimes)
    elif(SolveQueue(highestCheckIn,highestPollBooths,checkIn_rate,polling_rate)[0]==False):
        print("No feasible solutions exist. Recommended opening up another polling station in the precinct")
        lineTimes = SolveQueue(highestCheckIn,highestPollBooths,checkIn_rate,polling_rate)[1]
        plotQueue(lineTimes)
    else:
        #Bisection Search
        for i in range(0,len(resourceOptions)):
            x = math.ceil((a+b)/2)
            newCheckIn = int(resourceOptions[x][0])
            newPollBooth = int(resourceOptions[x][1])
            [feasible,lineTimes,qn] = SolveQueue(newCheckIn,newPollBooth,checkIn_rate,polling_rate)
            if (feasible==True and resourceOptions[x-1] in visited):
                plotQueue(lineTimes)
                print("Optimal Check-In Stations: ", newCheckIn)
                print("Optimal Polling Booths: ", newPollBooth)
                visualizeGraph(qn,newCheckIn,newPollBooth)
                qn.draw(fname="pollingGraph.png", figsize=(12, 3), bbox_inches='tight')
                break
            elif(feasible==True):
                b = x
            elif(feasible == False):
                a = x           
            visited.append(resourceOptions[x])

def plotQueue(lineTimes):
    time = np.linspace(0,13,len(lineTimes))
    plt.plot(time,lineTimes)
    n = 20 # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 0.65
    yy = signal.lfilter(b,a,lineTimes)
    plt.plot(time, yy, linewidth=2, linestyle="-", c="b")
    plt.xlabel('Time[hrs]')
    plt.ylabel('Wait Time [hrs]')
    plt.show()
    
    
def main():
  
    #User-specified inputs, comment this out for no input run
    checkIn_rate = float(input("How long does it take to check in a voter, in minutes?"))
    polling_rate = float(input("How long does it take the average voter to fill out their ballot, in minutes?"))
    cleaning_rate = float(input("How long does it take disinfect the polling booth, in minutes? "))
    num_checkIns = int(input("What is the maximum number of check-in booths the facility can set up?"))
    num_pollBooths = int(input("What is the maximum number of polling booths the facility can set up?"))
    
    global precinctPop
    precinctPop = int(input("What is the population in the precinct?"))
    userInputDemo = input("Do you want to input the demographics of the precinct? (Y/N)")
    if (userInputDemo == "Y"):  
        print("Input the percentage of each demographic. Ex: Input '45' for 45 percent")
        white = 10**-2*float(input("White: "))
        black = 10**-2*float(input("Black: "))
        hispanic = 10**-2*float(input("Hispanic: "))
        asian = 10**-2*float(input("Asian: "))
        nativeAmerican = 10**-2*float(input("Native American: "))
        mixed = 10**-2*float(input("Multiple Ethnicities:  "))
        middleEastern = 10**-2*float(input("Middle Eastern: "))
        other = 10**-2*float(input("Other: "))
    else: 
        white = 0.11
        black = 0.11
        hispanic = 0.11
        asian = 0.11
        nativeAmerican = 0.11
        mixed = 0.11
        other = 0.11
        middleEastern = 0.11
        
    #Default run, uncomment this for no input prompts
    #checkIn_rate = 2 #[min], average time to check-in
    #polling_rate = 6 #[min], average time to vote
    #cleaning_rate = 1
    #num_checkIns = 3
    #num_pollBooths = 5
    #global precinctPop
    #precinctPop = 500

    demographics = [white,black,hispanic,asian,nativeAmerican,mixed,other,middleEastern]   
    optimizeQueue(checkIn_rate,polling_rate,cleaning_rate,num_checkIns,num_pollBooths,precinctPop,demographics)

if __name__ == '__main__':
    main()
    