from numpy import random
import math
from core import Process, Processor

x = input('X: ')
y = input('Y: ')
z = input('Z: ')
sim_time = input('Time: ')
process_count = input('Desired process count: ')
k = input('Provide Process count minimum: ')
t1 = input('T1: ')
t2 = input('T2: ')
timer = 0

aux_list = []
for i in range(process_count):
    exp1 = random.exponential(x)
    exp2 = random.exponential(y)
    exp3 = random.exponential(z)
    uni = random.uniform()
    exp1 = math.ceil(exp1)
    exp2 = math.ceil(exp2)
    exp3 = math.ceil(exp3)
    priority = "High"
    if uni<0.7:
        priority = 'Low'
    elif uni<0.9:
        priority = 'Normal'

    process = Process(False,exp2,priority,exp3, exp1+timer)
    timer += exp1
    aux_list.append(process)

high = []
mid = []
low = []

for p in aux_list:
    if p.priority == 'High':
        high.append(p)
    elif p.priority == 'Normal':
        mid.append(p)
    else:
        low.append(p)

high.sort(key=lambda x: x.service_time, reverse=True)
mid.sort(key=lambda x: x.service_time, reverse=True)
low.sort(key=lambda x: x.service_time, reverse=True)

processor = Processor(t1, t2)
processor.init_queue.extend(high)
processor.init_queue.extend(mid)
processor.init_queue.extend(low)

while (not processor.is_empty) and (processor.clock<sim_time):
    if len(processor.FCFS)+len(processor.RR1)+len(processor.RR2):
        processor.job_loader()
    
