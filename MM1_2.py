# M/M/1 model  


import random 
import simpy 

random_seed = 101 
running_time = 60*8
interarrival_time = 5
service_time = 5.5

def update_total_time(increment):
    customer_generator.total_waiting_time += increment   

class Customer(object): 
    def __init__(self,env,counter,identity,time): 
        self.env=env 
        self.counter = counter 
        self.arrival_time=time
        self.customer_id = identity
        
        # customer arrives
        print('Customer%s arrived at %0.2f' %(self.customer_id,self.arrival_time)) 
        
        # updating total waiting time: 
        # note that it is possible that a customer does not enter the service     
        q = running_time - self.arrival_time
        update_total_time(q)
        
        # start waiting the service
        env.process(self.service())
    def service(self): 
        counter_request = self.counter.request()
        yield counter_request
        print('Customer%s waited %0.2f minutes; started service at %0.2f' %(self.customer_id,
                                                                            self.env.now-self.arrival_time,self.env.now))
        # updating total waiting time
        q = - (running_time - self.env.now)
        update_total_time(q)        
        
        #customer_generator.total_waiting_time = customer_generator.total_waiting_time - (running_time - self.env.now)
        # generating service time
        t = random.expovariate(1/ service_time)
        yield self.env.timeout(t) 
        print('Customer%s leaves the counter at %0.2f' %(self.customer_id,self.env.now))
        self.counter.release(counter_request)
          
def customer_generator(env,counter):  
    n=0
    customer_generator.total_waiting_time = 0 
    customer = Customer(env,counter,n,env.now)
    while True:       
        n = n + 1
        
        t = random.expovariate (1 / interarrival_time) # delay between arrivals            
         
        yield env.timeout(t)
        
        customer_generator.last_customer_id = n  # we update the total number of arrived customers                                         
                                                             
                                                 
        customer = Customer(env,counter,n,env.now) 
    
         

random.seed(random_seed)       

           
env=simpy.Environment()


counter = simpy.Resource(env, capacity=1)

env.process(customer_generator(env,counter))

env.run(running_time)

print('Total number of customers:%0.0f'%(customer_generator.last_customer_id+1))
print('Average waiting time:%0.2f'%(customer_generator.total_waiting_time/(customer_generator.last_customer_id+1)))