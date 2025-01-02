import numpy as np

# Toy neural netowrk, 1 hidden layer 
# SGD and Batch training plans to choose
# Ability to change learning rate along with decay algorithm

# TODO: multi hidden layer neural network capabilities  

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
        
        # TODO: finda a way to implement softmax implements               
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
            
    
    def __init__(self, num_i : int, num_h : int, num_o : int, learn_rate = 0.1, decay_rate = 0.01, activation = "sigmoid"): 
        
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
        
        self.weights_ih = np.random.uniform(-1, 1, size=(self.num_h, self.num_i))
        self.weights_ho = np.random.uniform(-1, 1, size=(self.num_o, self.num_h))
        
        self.bias_h = np.random.uniform(-1, 1, size=(self.num_h, 1))
        self.bias_o = np.random.uniform(-1, 1, size=(self.num_o, 1))
    
    # TODO: add softmax function for clamping data to percentages 
    @staticmethod
    def softmax(values : np.ndarray) -> np.ndarray: 
    
        return np.exp(values) / np.sum(np.exp(values), axis=0)
        
    @staticmethod
    def dsoftmax(values: np.ndarray) -> np.ndarray: 
    
        jacobian_matrix = np.diag(values) - np.outer(values, values)
        return jacobian_matrix  
    
    
    def predict_softmax(self, input): 
        
        return self.predict(input, True)
    
        
    def predict(self, input) -> np.ndarray: 

        input = np.array(input).reshape(-1, 1)

        h_value = (self.weights_ih @ input) + self.bias_h
        h_value = self.vec_func(h_value)
        
        o_value = (self.weights_ho @ h_value) + self.bias_o
        o_value = self.vec_func(o_value)
        
        return o_value 
    
    
    def __calc_hidden(self, inputs : np.ndarray) -> np.ndarray: 

        hidden = self.weights_ih @ inputs + self.bias_h
        return self.vec_func(hidden)
    
    
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
        
        hidden = self.__calc_hidden(inputs) 
        guess = self.predict(inputs)
        
        output_errors = expected_answers - guess
        
        gradient_output = self.__calc_gradient(output_errors, guess)

        weights_ho_transposed = np.transpose(self.weights_ho)
        
        weights_ho_delta = self.__calculate_delta_field(hidden, gradient_output, inputs.shape[1]) 
        
        self.__adjust_weights(self.weights_ho, self.bias_o, weights_ho_delta, gradient_output, inputs.shape[1])
        
        hidden_errors = weights_ho_transposed @ output_errors
        
        gradient_hidden = self.__calc_gradient(hidden_errors, hidden) 

        weights_ih_delta = self.__calculate_delta_field(inputs, gradient_hidden, inputs.shape[1]) 
        
        self.__adjust_weights(self.weights_ih, self.bias_h, weights_ih_delta, gradient_hidden, inputs.shape[1])
        
        self.epoch += 1

    # serialize model 
    def save_model(dir: str): 
        pass
    
    # deserialize model  
    def load_model(dir: str): 
        pass
    
        