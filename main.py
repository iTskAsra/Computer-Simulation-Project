from numpy import random
import math
from core import Process, Processor

x = int(input('X: '))
y = int(input('Y: '))
z = int(input('Z: '))
sim_time = int(input('Time: '))
process_count = int(input('Desired process count: '))
k = int(input('Provide Process count minimum: '))
t1 = int(input('T1: '))
t2 = int(input('T2: '))
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
    
    if processor.is_busy:
        processor.current_process.processed += 1

        if processor.current_process.previous_queue == 'High':
            if processor.current_process.processed>=processor.t1:
                processor.is_busy = False
                processor.RR2.append(processor.current_process)
                processor.current_process=None

        if processor.current_process.previous_queue == 'Normal':
            if processor.current_process.processed>=processor.t2:
                processor.is_busy = False
                processor.FCFS.append(processor.current_process)
                processor.current_process=None


        if processor.current_process.processed == processor.current_process.service_time:
            processor.is_busy = False
            processor.current_process = None

        for p in processor.FCFS:
            p.time_in_queue +=1

        for p in processor.RR1:
            p.time_in_queue +=1
        
        for p in processor.RR2:
            p.time_in_queue +=1

        for i in range(len(processor.FCFS)):
            if processor.FCFS[i].time_in_queue >= processor.FCFS[i].timeout:
                processor.processes_dropped += 1
                processor.FCFS.pop(i)

        for i in range(len(processor.RR1)):
            if processor.RR1[i].time_in_queue >= processor.RR1[i].timeout:
                processor.processes_dropped += 1
                processor.RR1.pop(i)
        
        for i in range(len(processor.RR2)):
            if processor.RR2[i].time_in_queue >= processor.RR2[i].timeout:
                processor.processes_dropped += 1
                processor.RR2.pop(i)

    if not processor.is_busy:
        disp = random.uniform()
        arg = 'Low'
        if disp < 0.8:
            arg = 'High'
        elif disp < 0.9:
            arg = 'Normal'

        processor.dispatcher(arg)

    processor.clock +=1
    
