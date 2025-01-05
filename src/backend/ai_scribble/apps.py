from django.apps import AppConfig
from .nm_manager import ModelManager

class AiScribbleConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_scribble'
    
    def ready(self):
        ModelManager.get_model("conv2D_number_model_1.keras") # test model convolutional for numbers with 80% + accuracy
        print(ModelManager.get_model().model_name_tag)
        return super().ready()
