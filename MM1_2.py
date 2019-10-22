# M/M/1 model 
# We did together in class 


import random 
import simpy 

random_seed = 101 
running_time = 60*8
interarrival_time = 5
service_time = 5.5

T=0
N=0

class Customer(object): 
    def __init__(self,env,counter,identity,time): 
        self.env=env 
        self.counter = counter 
        self.arrival_time=time
        self.customer_id = identity 
        print('Customer%s arrived at %0.2f' %(self.customer_id,self.arrival_time)) # customer arrives
        # updating total waiting time and the total number of customers
        global T
        T=T + (running_time - self.arrival_time)
        global N 
        N=self.customer_id       
        # start waiting the service
        env.process(self.service())
    def service(self): 
        counter_request = self.counter.request()
        yield counter_request
        print('Customer%s waited %0.2f minutes; started service at %0.2f' %(self.customer_id,
                                                                            self.env.now-self.arrival_time,self.env.now))
        # updating total waiting time
        global T
        T=T- (running_time - self.env.now)
        # generating service time
        t = random.expovariate(1/ service_time)
        yield self.env.timeout(t) 
        print('Customer%s leaves the counter at %0.2f' %(self.customer_id,self.env.now))
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

           
env=simpy.Environment()


counter = simpy.Resource(env, capacity=1)

env.process(customer_generator(env,counter))

env.run(running_time)

print('Total number of customers:%0.0f'%(N+1))
print('Average waiting time:%0.2f'%(T/(N+1)))

