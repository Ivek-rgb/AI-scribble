from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.neural_networks.data_prep import DataLoader
from .nm_manager import ModelManager
from django.http import JsonResponse
import json

@api_view(['GET', 'POST'])
def process_request(request) -> Response:
    
    if request.method == 'GET':
        #ModelManager.get_model(request.GET.get("model_name")) # process model change request  
        return Response({"name": ModelManager.get_model().model_name_tag }) # test run for getting the model name correctly 
    
    elif request.method == 'POST':
        
        data_sent = json.loads(request.body.decode('utf-8'))
        

        
        image_data = data_sent.get('image')
        np_array = DataLoader.b64_img_to_nparr(image_data)
        np_array = DataLoader.numpy_array_mapper(np_array, lambda x: x / 255)
        output = ModelManager.predict(np_array)
        output : list = output.tolist()[0]
        
        print(output)
        
        return Response({"prediction" : f"{ModelManager._categories_map[output.index(max(output))]}"  })
    

# TODO: implement function that reads trained categories and return's ones that 
def get_random_label(request): 
    return Response()

# TODO: function that will grab single data array and then feed it to model  
def process_image_and_return_prediction(image_data): 
    return Response() 
