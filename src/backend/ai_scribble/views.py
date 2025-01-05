from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .nm_manager import ModelManager
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def process_request(request) -> Response:
    
    if request.method == 'GET':
        ModelManager.get_model(request.GET.get("model_name")) # process model change request  

    elif request.method == 'POST':
        pass


# TODO: implement function that reads trained categories and return's ones that 
def get_random_label(request): 
    return Response()

# TODO: function that will grab single data array and then feed it to model  
def process_image_and_return_prediction(): 
    return Response() 



