from django.apps import AppConfig
from .nm_manager import ModelManager

class AiScribbleConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_scribble'
    
    def ready(self):
        ModelManager.load_all_models()
        print(ModelManager._model_list)
<<<<<<< HEAD
        ModelManager.get_model('conv2d_scribble_50_categories_augmented_1') # default loaded model 
=======
        ModelManager.set_model('conv2D_mnist_low_training_augmented') # default loaded model 
>>>>>>> cd7c868 (features)
        ModelManager.load_categories() # default loaded data
        return super().ready()
