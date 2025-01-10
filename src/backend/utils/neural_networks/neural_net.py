import numpy as np

# Toy neural netowrk, 1 hidden layer 
# SGD and Batch training plans to choose
# Ability to change learning rate along with decay algorithm

class ToyNeuralNetwork: 
    
    class __ActivationFunction: 
        
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance 
            self.function = None
            self.dfunction = None
            self.sigmoid()
            
        def update_functions(self): 
            self.outer_instance.vec_func = np.vectorize(self.function)
            self.outer_instance.vec_dfunc = np.vectorize(self.dfunction)
            
        def sigmoid(self):
            self.function = lambda x: 1 / (1 + np.exp(-x))
            self.dfunction = lambda y: y * (1 - y)
            self.update_functions()
            self.outer_instance.activation = "sigmoid"
                        
        def relu(self): 
            self.function = lambda x : max(0, x)
            self.dfunction = lambda y : 0. if y < 0. else 1.
            self.update_functions()
            self.outer_instance.activation = "relu"
        
        def softmax(self): 
            self.outer_instance.activation = "softmax"   
        
    class __DecayFunction: 
        
        def __init__(self, outer_instance, decay_rate): 
            self.outer_instance = outer_instance
            self.decay_rate = decay_rate
            self.decay_function = None
            self.exponentional_decay() 
        
        def change_decay_rate(self, new_decay_rate): 
            self.outer_instance.decay_rate = new_decay_rate
            self.decay_rate = new_decay_rate
        
        def exponentional_decay(self): 
            self.decay_function = lambda x, y: x * np.exp( - self.decay_rate * y) 
        
    def __init__(self, num_i : int, num_h : tuple[int], num_o : int, learn_rate = 0.1, decay_rate = 0.01, activation = "sigmoid"): 
        
        self.num_i = num_i
        self.num_h = num_h
        self.num_o = num_o
        
        self.vec_func = None
        self.vec_dfunc = None
        
        self.epoch = 0 
        
        self.a_func =  self.__ActivationFunction(self)
        
        self.decay_control = self.__DecayFunction(self, decay_rate) 
        
        self.activation = activation
        self.learn_rate = learn_rate
        
        self.weights_ih = np.random.uniform(-1, 1, size=(self.num_h[0], self.num_i))
        
        self.weights_hh = [
            
            np.random.uniform(-1, 1, size=(self.num_h[i + 1], self.num_h[i])) for i in range(len(num_h) - 1)
        
        ]
        
        self.weights_ho = np.random.uniform(-1, 1, size=(self.num_o, self.num_h[len(self.num_h) - 1]))
        
        self.bias_h =  [ np.random.uniform(-1, 1, size=(i, 1)) for i in self.num_h ]
        self.bias_o = np.random.uniform(-1, 1, size=(self.num_o, 1))
        
    
    # TODO: add softmax function for clamping data to percentages 
    @staticmethod
    def softmax(values : np.ndarray) -> np.ndarray: 
    
        return np.exp(values) / np.sum(np.exp(values), axis=0)
        
    @staticmethod
    def dsoftmax(values: np.ndarray) -> np.ndarray: 
    
        jacobian_matrix = np.diag(values) - np.outer(values, values)
        return jacobian_matrix  
    
    
    def dropout(self, activations : np.ndarray, rate):
    
        mask = (np.random.rand(*activations.shape) > rate).astype(float)
        return activations * mask / (1 - rate)  
    
    
    def _forward_pass(self, inputs): 
        
        inputs = np.array(inputs).reshape(-1, 1)
        
        activations = [inputs]
        
        h_value = self.vec_func((self.weights_ih @ inputs) + self.bias_h[0])
        
        activations.append(h_value)
        
        for i in range(len(self.weights_hh)): 
            h_value = self.vec_func((self.weights_hh[i] @ h_value) + self.bias_h[i + 1])
            h_value = self.dropout(h_value, 0.001) # TODO: add dropout range to shizzle fadizzle 
            activations.append(h_value)
        
        activations.append(self.vec_func((self.weights_ho @ h_value) + self.bias_o))
        
        return activations
        
    def predict(self, inputs) -> np.ndarray: 

        return self._forward_pass(inputs)[-1]
    
    def __calc_gradient(self, errors : np.ndarray, guess_arr : np.ndarray) -> np.ndarray: 

        gradient_output = self.vec_dfunc(guess_arr) * errors 
        return gradient_output * self.learn_rate
    
    
    @staticmethod
    def __adjust_weights(weights_ref : np.ndarray, bias_ref : np.ndarray, weights_delta : np.ndarray, gradient_ref : np.ndarray, inputs_size : int) -> np.ndarray: 
        
        weights_ref += weights_delta
        bias_ref += np.sum(gradient_ref, axis=1, keepdims=True) / inputs_size
        
        
    @staticmethod 
    def __calculate_delta_field(weights_ref : np.ndarray, gradient_field : np.ndarray, inputs_size : int) -> np.ndarray: 
        
        return gradient_field @ np.transpose(weights_ref) / inputs_size

    
    def reset_epoch(self): 
        
        self.epoch = 0

    def train(self, inputs, expected_answers) -> None: 
        
        self.learn_rate = self.decay_control.decay_function(self.learn_rate, self.epoch) 
        
        inputs = np.array(inputs).reshape(-1, 1)
        expected_answers = np.array(expected_answers).reshape(-1, 1)
        
        activations = self._forward_pass(inputs)
                
        hidden = activations[-2] 
        guess = activations[-1]
        
        output_errors = expected_answers - activations[-1]
        
        gradient_output = self.__calc_gradient(output_errors, guess)

        weights_ho_delta = self.__calculate_delta_field(hidden, gradient_output, inputs.shape[1]) 
        
        self.__adjust_weights(self.weights_ho, self.bias_o, weights_ho_delta, gradient_output, inputs.shape[1])
        
        hidden_errors = np.transpose(self.weights_ho) @ output_errors
        
        for i in range(len(self.weights_hh) -1, -1, -1): 

            gradient_hidden = self.__calc_gradient(hidden_errors, activations[i + 2])
            weights_hh_delta = self.__calculate_delta_field(activations[i + 1], gradient_hidden, inputs.shape[1])
            
            self.__adjust_weights(self.weights_hh[i], self.bias_h[i + 1], weights_hh_delta, gradient_hidden, inputs.shape[1]); 
            hidden_errors = np.transpose(self.weights_hh[i]) @ hidden_errors
        
        gradient_hidden = self.__calc_gradient(hidden_errors, activations[1]) 

        weights_ih_delta = self.__calculate_delta_field(inputs, gradient_hidden, inputs.shape[1]) 
        
        self.__adjust_weights(self.weights_ih, self.bias_h[0], weights_ih_delta, gradient_hidden, inputs.shape[1])
        
        self.epoch += 1

    # serialize model 
    def save_model(dir: str): 
        pass
    
    # deserialize model  
    def load_model(dir: str): 
        pass
    
        