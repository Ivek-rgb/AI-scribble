from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def process_request(request) -> Response: 
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass

def get_random_label(): 
    return Response()

def process_image_and_return_prediction(): 
    return Response() 

# might be implemented later for multiple model changes 
def model_change(): 
    pass

