from threading import Lock
from utils.neural_networks.neural_models import NeuralModels
import os 

class ModelManager:
    
    _neural_model : NeuralModels = NeuralModels()
    _current_model_name = None  
    _lock = Lock()
    
    MODEL_PATH = '../models/'    

    @classmethod 
    def generate_path(cls, model_name): 
        return os.path.join(os.path.dirname(__file__), f'{cls.MODEL_PATH}{model_name}')
    
    @classmethod
    def get_model(cls, model_name = None): 
        with cls._lock: 
            if model_name == None: return cls._neural_model
            if cls._neural_model.model_name_tag != model_name: 
                cls._neural_model.load_model(cls.generate_path(model_name)) 
                cls._current_model_name = cls._neural_model.model_name_tag
            return cls._neural_model
        
    @classmethod 
    def save_model(cls): 
        with cls._lock: 
            cls._neural_model.save_model(cls.generate_path(''))
            
    @classmethod 
    def predict(cls, prediction_data): 
        with cls._lock: 
            return cls._neural_model.predict(prediction_data) 
            
    @classmethod
    def reset_model(cls): 
        with cls._lock:
            cls._neural_model = NeuralModels()