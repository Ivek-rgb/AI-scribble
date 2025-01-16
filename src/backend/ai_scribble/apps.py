from django.apps import AppConfig
from .nm_manager import ModelManager

class AiScribbleConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_scribble'
    
    def ready(self):
        ModelManager.load_all_models()
        print(ModelManager._model_list)
        ModelManager.set_model('conv2d_scribble_50_categories_augmented_1') # default loaded model 
        ModelManager.load_categories() # default loaded data
        return super().ready()
