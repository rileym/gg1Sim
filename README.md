# gg1Sim

This is a g/g/1 queue simulation I wrote for a simulation class (See http://en.wikipedia.org/wiki/G/G/1_queue). The purpose of the exercise was to demonstrate the sensitivity of certain performance metrics to assumptions about "input distribution", in this case the metric was mean queue length and the input distribution was the distribution of inter-arrival times. I had learned basic python the week before this assigment so took the exercise as an opportunity to further familiarize myself with python in general and its object oriented pyhton in particular. Note too that we were not allowed to use any high level packages or routines in this assigment, e.g., no numpy, scipy.

Specifics of the queue simulation:

We were to estimate L (the average queue length over the fixed time time period) for a g/g/1 queue with service times distributed as the sum of two independent uniform random varaibles (distribution looks like a triange) and with each of the following inter-arrival time distributions: exponetial, weibul (2x: once for each of two different parameters), and auto-corrlated normal random variables (2x: once for postive and once for negative correlation. The formal model behind this simulation is a "generalized semi-markov process" (GSMP) which is a stocastic process description of discrete event system. 




