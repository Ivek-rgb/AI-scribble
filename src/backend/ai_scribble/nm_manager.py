from threading import Lock
from utils.neural_networks.neural_models import NeuralModels
from utils.neural_networks.data_prep import DataLoader
import os


class ModelManager:

    _neural_model: NeuralModels = NeuralModels()
    _current_model_name = None
    _model_list: list[str] = []
    _lock = Lock()
    _categories_map = {}

    MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/')
    CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), '../data/')

    @classmethod
    def generate_path_model(cls, model_name):
        return os.path.join(cls.MODEL_PATH, f'{model_name}.keras')

    @classmethod
    def generate_path_categories(cls, category_file_name):
        return os.path.join(cls.CATEGORIES_PATH, f'{category_file_name}.txt')

    @classmethod
    def load_all_models(cls):
        with cls._lock:
            cls._model_list = list(map(lambda x: os.path.splitext(os.path.basename(x))[
                                   0], DataLoader.get_all_files_from_dir(cls.MODEL_PATH, ".keras")))

    @classmethod
    def get_model(cls):
        with cls._lock:
            return cls._neural_model

    @classmethod
    def set_model(cls, model_name=None):
        with cls._lock:
            if model_name == cls._neural_model.model_name_tag:
                return cls._neural_model
            elif cls._neural_model.model_name_tag != model_name:
                cls._neural_model.load_model(
                    cls.generate_path_model(model_name))
                cls._current_model_name = cls._neural_model.model_name_tag
                # cls.load_categories()
            return cls._neural_model

    @classmethod
    def get_available_models(cls):
        with cls._lock:
            return cls._model_list

    @classmethod
    def load_categories(cls, categories_file_name=None):
        with cls._lock:
            path = cls.generate_path_categories(
                categories_file_name if categories_file_name else cls._neural_model.model_name_tag)
            cls._categories_map = DataLoader.load_categories_static(
                path, False)

    @classmethod
    def save_model(cls):
        with cls._lock:
            cls._neural_model.save_model(
                cls.generate_path_model(cls._neural_model.model_name_tag))

    @classmethod
    def predict(cls, prediction_data):
        with cls._lock:
            return cls._neural_model.predict(prediction_data)

    @classmethod
    def reset_model(cls):
        with cls._lock:
            cls._neural_model = NeuralModels()
