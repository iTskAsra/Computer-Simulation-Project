from numpy import random

class Process:
    def __init__(self, dropped=False, service_time=0, priority='Low',timeout=0, arrival=0,processed=0) -> None:
        self.dropped = dropped
        self.service_time = service_time
        self.priority = priority
        self.timeout = timeout
        self.time_in_queue = 0
        self.arrival = arrival
        self.processed = processed
        self.previous_queue = 'High'

    def __str__(self) -> str:
        return f'Service time:{self.service_time}, Priority: {self.priority}, Arrival: {self.arrival}, Timeout: {self.timeout}'


class Processor:
    def __init__(self, t1, t2) -> None:
        self.clock = 0
        self.is_busy = False
        self.is_empty = False
        self.RR1 = []
        self.RR2 = []
        self.FCFS = []
        self.rr1_accumulated = 0
        self.rr2_accumulated = 0
        self.fcfs_accumulated = 0
        self.t1 = t1
        self.t2 = t2
        self.processes_dropped = 0
        self.init_queue = []
        self.current_process = None
        self.finished_or_dropped_processes = []

    def dispatcher(self, queue='Low'):
        p = None
        if queue == 'High' and len(self.RR1)>0:
            p = self.RR1.pop(0)
        elif queue == 'Normal' and len(self.RR2)>0:
            p = self.RR2.pop(0)
        elif len(self.FCFS)>0:
            p = self.FCFS.pop(0)
        elif len(self.init_queue)==0:
            self.is_empty = True
        
        if p:
            self.current_process = p
            self.is_busy = True

    def job_creator():
        pass

    def job_loader(self, k):
        counter=0
        length = len(self.init_queue)
        i=0
        while i<length:
            length = len(self.init_queue)
            if i==length:
                break
            p = self.init_queue[i]
            if p.arrival <= self.clock:
                self.RR1.append(p)
                self.init_queue.pop(i)
                counter += 1
            if counter == k:
                break

            i+=1
        

