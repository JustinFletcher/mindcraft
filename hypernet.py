# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 01:23:14 2016

@author: Justin Fletcher
"""

import numpy

#
#class Mind(object):
#    
#    
#class NeuralNetwork(super Mind):
#    
#class ContinuousSimAnnealRNN(super NeuralNetwork):
#    
class HyperNet(object):

    def __init__(self, input_size, output_size, num_neurons, upper_graph=()):
        
        if (num_neurons < input_size) or (num_neurons < input_size):
             raise "huh?"
        
        # If not inititialized with an upper graph, this is the top of the net.
        if not upper_graph:
            
            # construct a random weight matrix for the top graph.
            self.upperGraph.w = numpy.random.rand(num_neurons, num_neurons)
            
        else:
            self.upperGraph = upper_graph
        
        # Construct a lower graph of the indicated size.        
        self.lowerGraph.w = numpy.random.rand(num_neurons, num_neurons**2)
    
    def step(self, num_steps=1):
        
        for step in range(0,num_steps):
            
            self.upperGraph.w = self.lowerGraph.prop(self.upperGraph.state)
       
       
       # What id the lower graph "provided pressure" on the weights of the 
       # graph, rather than changing them directly... You lose generality, as 
       # that pressure is a specific way to implement the effect of the 
       # computation perfromed by the lower graph, which could in principle be
       # encoded into the function represented by that graph.
       
       # To control graph size explosion, consider weight sharing, or partial
       # graph evolutions. Note that evolutionary algorithms are not 
       # fundamental, as they are instantiations of gradient descent. 
       # Specifally, descent on a constantly undulating fitness landscape.
       # Gradient descent, either implicit or explicit is also not fundamental,
       # as it is a sequence of compuations - however, gradient descent, in the
       # guise of least-action, is the only known computation performed 
       # by the univers, and therefore seems a good place to stop.
       
    
    