from django.apps import AppConfig
from .nm_manager import ModelManager

class AiScribbleConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_scribble'
    
    def ready(self):
        ModelManager.get_model('conv2d_emnist_letters_augmented_1')
        ModelManager.load_categories()
        print(ModelManager.get_model().model_name_tag)
        print("App loading ready")
        return super().ready()
