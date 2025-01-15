from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.neural_networks.data_prep import DataLoader
from .nm_manager import ModelManager
from django.http import JsonResponse
import json

# print(ModelManager._model_list) -- ispis mogucih modela 
# ModelManager.get_model('conv2D_mnist_low_training_augmented') # primjer mijenjanja modela prek teksta
# ModelManager.load_categories('new_number_data') # poziv funkcije za učitavanje kateogrija, 
# ak se ne preda filename pretpostavlja se ime modela za category filename

@api_view(['GET', 'POST'])
def process_request(request) -> Response:
    
    if request.method == 'GET':
        
        return JsonResponse({ 'current-model': ModelManager.get_model().model_name_tag, 'models' : ModelManager.get_available_models()})
    
    elif request.method == 'POST':
        
        data_sent = json.loads(request.body.decode('utf-8'))
        
        image_data = data_sent.get('image')
        np_array = DataLoader.b64_img_to_nparr(image_data)
        np_array = DataLoader.numpy_array_mapper(np_array, lambda x: x / 255)
        output = ModelManager.predict(np_array)
        output : list = output.tolist()[0]
        
        print(output)
        
        return JsonResponse({"prediction" : f"{ModelManager._categories_map[output.index(max(output))]}"  })

def get_random_label(request): 
    return Response()

def process_image_and_return_prediction(image_data): 
    return Response() 
