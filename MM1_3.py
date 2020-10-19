# M/M/1 model 


import random 
import simpy 
import matplotlib
import matplotlib.pyplot as plt
  
random_seed = 101 
running_time = 60*6
interarrival_time = 5
service_time = 5.5


class Customer(object): 
    
    def __init__(self,env,counter,identity,time): 
        self.env=env 
        self.counter = counter 
        self.arrival_time=time
        self.customer_id = identity 

        env.process(self.service())
   
    def service(self): 
        counter_request = self.counter.request()
        yield counter_request
       ###
        global N 
        N=self.customer_id        
       
        t = random.expovariate(1/ service_time)
        yield self.env.timeout(t) 
        
        self.counter.release(counter_request)
        
def customer_generator(env,counter):  
    n=0
    customer = Customer(env,counter,n,env.now)
    while True:       
        n = n + 1 
        t = random.expovariate (1 / interarrival_time) # delay between arrivals 
        yield env.timeout(t)
        customer = Customer(env,counter,n,env.now) 
         

random.seed(random_seed)       

R=25
X = range(0,R)
Y = []

for i in X: 
             
    env=simpy.Environment()

    counter = simpy.Resource(env, capacity=1)

    env.process(customer_generator(env,counter))

    env.run(running_time)

    Y.append(N+1)

S=0; 
    
for i in X: 
    
    S=S+Y[i]

print('%0.2f'%(S/R))    

plt.plot(X,Y,"-o")
plt.ylabel("Total number of customers")
plt.xlabel("Simulation runs")
plt.show()