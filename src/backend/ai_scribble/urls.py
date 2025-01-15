from django.urls import path
from .views import process_guess_request, process_models_request

urlpatterns = [
    path('guess', process_guess_request),
    path('models', process_models_request)
]
