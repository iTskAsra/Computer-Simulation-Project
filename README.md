# CPU Scheduler Simulation

This project, as part of Dr. Safai's Computer Simulation course at the Faculty of Computer Engineering, simulates a CPU scheduler using a discrete event simulation approach. The simulation involves a two-layer queue system to manage processes as they await CPU time. This project was undertaken during the first semester of the academic year 1401-1402.

## Table of Contents

- [System Description](#system-description)
- [Implementation Details](#implementation-details)
- [Inputs and Outputs](#inputs-and-outputs)

## System Description

The simulation mimics a CPU scheduler where processes transition through queues to reach the CPU core. The queue system comprises two layers: a priority queue and three different policy queues. Processes initially enter the priority queue and are then transferred to the second layer based on their priority.

## Implementation Details

- **Task Creation**: The `JobCreator` method generates input tasks following a Poisson process with rate X. Tasks have a service time derived from an exponential distribution with mean Y and are assigned a priority (Low, Normal, High) randomly as per given probabilities.
- **Transfer to Second Layer**: The `JobLoader` method checks the total number of tasks at fixed intervals and transfers tasks to the second layer if the number of tasks is less than a threshold value.
- **Task Execution**: The `Dispatcher` method handles the task execution process by selecting a queue from the second layer based on the task priority and queue policy, and provides the task to the processor.

### Queue Policies

- **FCFS (First Come First Serve)**: A FIFO queue.
- **1T-Round-Robin**: Like FCFS but limits the processor execution time for each task to 1T time units.
- **2T-Round-Robin**: Similar to 1T-Round-Robin but with a different execution time limit.

