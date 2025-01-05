from keras.src.models import Sequential
from keras.src.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from keras.api.saving import load_model
import tensorflow as tf
import numpy as np
import os 

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class NeuralModelError(Exception): 
    def __init__(self, message):
        self.message = message
        super.__init__(self.message)

class NeuralModels: 
    
    FILE_EXTENSION = '.keras'
    
    def __init__(self, model = None, model_name_tag = None): 
        self.model = model
        self.model_name_tag = model_name_tag 
    
    @staticmethod
    def equalize_list_lens(equalize: list, equalize_to_len: int, min_dif: int = 0, pattern_getter = lambda list: list[-1]): 
        while len(equalize) < equalize_to_len - min_dif: 
            equalize.append(pattern_getter(equalize))
        
        return equalize 
    
    @staticmethod
    def custom_seq_model_empty() -> Sequential: 
        return Sequential() 
    
    @staticmethod
    def debug_GPU_devices() -> None: 
        print(tf.config.list_physical_devices('GPU'))
    
    # sets the inner container for model to a desired model 
    def set_model(self, created_model):
        self.model = created_model    
    
    # creates a new multi layer fully connected neural network     
    def mlp_model(self, layers_rep: tuple[int], activation_function: list[str], dropout_values: list[int]): 

        self.model = Sequential()
        
        if len(layers_rep) < 3: 
            raise NeuralModelError("error in number of layers - sequential model requires input, atleast 1 hidden and an ouput layer")

        activation_function = self.equalize_list_lens(activation_function, len(layers_rep), 1)
        dropout_values = self.equalize_list_lens(dropout_values, len(layers_rep), 1)
        dropout_values[-1] = 0
        
        self.model.add(Dense(units=layers_rep[1], activation=activation_function[0], input_dim=layers_rep[0]))
        self.model.add(Dropout(dropout_values[0]))
        for i in range(2, len(layers_rep)): 
            self.model.add(Dense(units=layers_rep[i], activation=activation_function[i - 1]))
            self.model.add(Dropout(dropout_values[i - 1]))
    
    
    # creates a convolutional 2D network from a template  
    def conv2D_model(self, input_shape: tuple[int], filter_layers: tuple[int], kernel_size_per_layers: list[tuple[int]], pool_size: tuple[int], 
                   activation_functions: list[str], layers_rep: tuple[int], dropout_values : list[int], batch_normalization: bool = False): 
        
        self.model = Sequential()
        
        if len(layers_rep) < 1: 
            raise NeuralModelError("error in number of layers - convolutional model requires atleast one layer for output")

        activation_functions = self.equalize_list_lens(activation_functions, len(filter_layers) + len(layers_rep), 1)
        kernel_size_per_layers = self.equalize_list_lens(kernel_size_per_layers, len(filter_layers))
        dropout_values = self.equalize_list_lens(dropout_values, len(layers_rep) + 1)
        
        dropout_values[-1] = 0
        
        self.model.add(Conv2D(filter_layers[0], kernel_size=kernel_size_per_layers[0], activation=activation_functions[0], input_shape=input_shape))
        a_func_i = 1
        
        if batch_normalization: 
            self.model.add(BatchNormalization())
        
        for i in range(1, len(filter_layers)): 
            self.model.add(Conv2D(filter_layers[i], kernel_size=kernel_size_per_layers[i], activation=activation_functions[a_func_i]))
            a_func_i += 1
            
        self.model.add(MaxPooling2D(pool_size=pool_size))
        self.model.add(Dropout(dropout_values[0]))        
        self.model.add(Flatten())
        
        for i in range(len(layers_rep)): 
            self.model.add(Dense(layers_rep[i], activation=activation_functions[a_func_i]))
            self.model.add(Dropout(dropout_values[i + 1]))
            a_func_i += 1

    # compiles sequential models and prepares them for use         
    def model_compile(self, optimizer : str = 'adam', loss_type : str = 'categorical_crossentropy', metrics: list[str] = ['accuracy']): 
        self.model.compile(
            optimizer= optimizer,
            loss= loss_type,
            metrics=[*metrics]
        )
        
    # train model on given batch of data and labels for correction 
    def fit(self, training_data: np.ndarray, training_labels: np.ndarray, batch_size: int = 64, epochs: int = 10, verbose: int = 0): 
        self.model.fit(training_data, training_labels, batch_size=batch_size, epochs=epochs, verbose=verbose)
    
    # return model's prediciton based on it's configuration   
    def predict(self, prediction_data : np.ndarray, verbose = 0) -> np.ndarray: 
        return self.model.predict(prediction_data, verbose=verbose)
    
    # TODO: prompt user if the model has not been saved yet / add desc for this functions 
    def save_model(self, path, verbose = 0): 
        path_to_save = path + self.model_name_tag + self.FILE_EXTENSION
        self.model.save(path_to_save)
        if verbose: print(f"DEBUG: model saved at - {path_to_save}")
        
    def save_as_model(self, path, new_name, verbose = 0): 
        self.model_name_tag = new_name
        self.save_model(path, verbose)
    
    def load_model(self, path, verbose = 0): 
        self.model = load_model(path)
        self.model_name_tag = os.path.splitext(os.path.basename(path))[0]
        if verbose : print(f"DEBUG: model loaded - name: {self.model_name_tag}")
    