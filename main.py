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
processor_runtime = 0

while (not processor.is_empty) and (processor.clock<sim_time):
    if (len(processor.FCFS)+len(processor.RR1)+len(processor.RR2))<k:
        processor.job_loader(k)
    
    if processor.is_busy:
        processor_runtime += 1
        processor.current_process.processed += 1

        if processor.current_process.previous_queue == 'High':
            if processor.current_process.processed>=processor.t1:
                processor.is_busy = False
                processor.RR2.append(processor.current_process)
                processor.current_process=None
        elif processor.current_process.previous_queue == 'Normal':
            if processor.current_process.processed>=processor.t2:
                processor.is_busy = False
                processor.FCFS.append(processor.current_process)
                processor.current_process=None


            if processor.current_process.processed >= processor.current_process.service_time:
                processor.is_busy = False
                processor.finished_or_dropped_processes.append(processor.current_process)
                processor.current_process = None

        for p in processor.FCFS:
            p.time_in_queue +=1

        for p in processor.RR1:
            p.time_in_queue +=1
        
        for p in processor.RR2:
            p.time_in_queue +=1

        length = len(processor.FCFS)
        i=0
        while i<length:
            if processor.FCFS[i].time_in_queue >= processor.FCFS[i].timeout:
                processor.processes_dropped += 1
                processor.finished_or_dropped_processes.append(processor.FCFS.pop(i))
            length = len(processor.FCFS)
            i+=1

        i=0
        length = len(processor.RR1)
        while i<length:
            if processor.RR1[i].time_in_queue >= processor.RR1[i].timeout:
                processor.processes_dropped += 1
                processor.finished_or_dropped_processes.append(processor.RR1.pop(i))
            length = len(processor.RR1)
            i+=1
        
        i=0
        length = len(processor.RR2)
        while i<length:
            if processor.RR2[i].time_in_queue >= processor.RR2[i].timeout:
                processor.processes_dropped += 1
                processor.finished_or_dropped_processes.append(processor.RR2.pop(i))
            i+=1
            length = len(processor.RR2)

    if not processor.is_busy:
        disp = random.uniform()
        arg = 'Low'
        if disp < 0.8:
            arg = 'High'
        elif disp < 0.9:
            arg = 'Normal'

        processor.dispatcher(arg)

    processor.rr1_accumulated += len(processor.RR1)
    processor.rr2_accumulated += len(processor.RR2)
    processor.fcfs_accumulated += len(processor.FCFS)

    processor.clock +=1
    
print(f'CPU Utilization is {processor_runtime/processor.clock * 100}%')

accumulated_queue_time = 0
for i in range(len(processor.finished_or_dropped_processes)):
    print(f'Process {i+1} has spent {processor.finished_or_dropped_processes[i].time_in_queue} seconds in a queue')
    accumulated_queue_time += processor.finished_or_dropped_processes[i].time_in_queue

print(f'Average time spent in a queue is {accumulated_queue_time/len(processor.finished_or_dropped_processes)}')
print(f'Average length of the RR1 queue is {processor.rr1_accumulated/processor.clock}')
print(f'Average length of the RR2 queue is {processor.rr2_accumulated/processor.clock}')
print(f'Average length of the FCFS queue is {processor.fcfs_accumulated/processor.clock}')
print(f'{processor.processes_dropped/process_count * 100}% of the processes were dropped by the processor.')