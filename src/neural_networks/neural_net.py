import math
import numpy as np
import random as rand
import json
import os
        
class __ActivationFunction: 
    
    def __init__(self, function, functiond):
        #self.outer_instance = outer_instance 
        self.function = function
        self.dfunction = functiond
        #self.sigmoid()
        
    def update_functions(self): 
        self.outer_instance.vec_func = np.vectorize(self.function)
        self.outer_instance.vec_dfunc = np.vectorize(self.dfunction)
        
    def sigmoid(self):
        self.function = lambda x: 1 / (1 + np.exp(-x))
        self.dfunction = lambda y: y * (1 - y)
        self.update_functions()
        #self.outer_instance.activation = "sigmoid"
                    
    def relu(self): 
        self.function = lambda x : max(0, x)
        self.dfunction = lambda y : 0. if y < 0. else 1.
        self.update_functions()
        #self.outer_instance.activation = "relu"
    
    def softmax(self): 
        #self.outer_instance.activation = "softmax" # TODO: overflow fix for softmax activation function required 
        pass

class ToyNeuralNetwork: 

    activation_functions = {
        "sigmoid" : __ActivationFunction(lambda x: 1 / (1 + np.exp(-x)), lambda y: y * (1 - y)),
        "relu": __ActivationFunction(...)
    }       
    
    def __init__(self, num_i : int, num_h : int, num_o : int, learn_rate = 0.1, activation = "sigmoid"): 
        
        self.num_i = num_i
        self.num_h = num_h
        self.num_o = num_o
        
        self.vec_func = self.activation_functions[activation].function
        self.vec_dfunc = self.activation_functions[activation].dfunction
        
        #self.a_func =  self.activation_functions[activation]
        
        self.activation = activation
        if activation == "softmax":
            self.vec_func_output = lambda x: np.exp(x) / np.sum(np.exp(x))
        
        self.learn_rate = learn_rate
        
        self.weights_ih = np.random.uniform(-1, 1, size=(self.num_h, self.num_i))
        self.weights_ho = np.random.uniform(-1, 1, size=(self.num_o, self.num_h))
        
        self.bias_h = np.random.uniform(-1, 1, size=(self.num_h, 1))
        self.bias_o = np.random.uniform(-1, 1, size=(self.num_o, 1))
        
        
    def predict(self, input): 

        input = np.array(input).reshape(-1, 1)

        h_value = self.weights_ih @ input
        h_value += self.bias_h
        h_value = self.vec_func(h_value)
        
        o_value = self.weights_ho @ h_value 
        o_value += self.bias_o
        
        if self.activation == "softmax":
            o_value = np.exp(o_value) / np.sum(np.exp(o_value))
        else:
            o_value = self.vec_func(o_value)
        return o_value
    
    def train(self, inputs, expected_answer): 
        
        inputs = np.array(inputs).reshape(-1, 1)
        expected_answer = np.array(expected_answer).reshape(-1, 1)

        hidden = self.weights_ih @ inputs
        hidden += self.bias_h
        
        hidden = self.vec_func(hidden)

        guess = self.predict(inputs)
        
        output_errors = expected_answer - guess
        
        gradient_output = self.vec_dfunc(guess) * output_errors 
        gradient_output *= self.learn_rate        

        weights_ho_transposed = np.transpose(self.weights_ho)

        hidden_errors = weights_ho_transposed @ output_errors
        
        weights_ho_delta =  gradient_output @ np.transpose(hidden)
        
        self.weights_ho += weights_ho_delta
        self.bias_o += gradient_output
        
        hidden_gradient = self.vec_dfunc(hidden) * hidden_errors
        hidden_gradient *= self.learn_rate
        
        weights_ih_transposed = np.transpose(inputs)
        weigths_ih_delta = hidden_gradient @ weights_ih_transposed
        
        self.weights_ih += weigths_ih_delta
        self.bias_h += hidden_gradient

    # TODO: 50/50 to add feature, sequential training works good for small model like this     
    def train_batch():
        pass
    
    def toJSON(self):
        print(self.num_i)
        print(self.num_h)
        print(self.num_o)
        print(self.vec_func)
        print(self.vec_dfunc)
        #print(self.a_func)
        print(self.activation)
        print(self.learn_rate)
        print(self.weights_ih)
        print(self.weights_ho)
        print(self.bias_h)
        print(self.bias_o)
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

    # serialize model 
    def save_model(self): 
        jsonFile = self.toJSON()
        home_dir = os.path.expanduser("~")
        file_path = os.path.join(home_dir, "neuralNetworkData.json")
        f = open(file_path, "w")
        f.write(jsonFile)
        f.close()
        pass
    
    # deserialize model  
    def load_model(dir: str): 
        pass
    
        