
import os
import csv
import math
import base64
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO

# 28*28 - image resolution, both for numbers and doodles   

class DataLoader:

    def __init__(self, path):
        self.path = path
        self.data = None

    def load_data_npy(self, reshape_to_2828 : bool = False, append = True): 
        data = []
        files = [file for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file)) and os.path.splitext(file)[1] == '.npy']
        for file in files:
            loaded_np_rep = np.load(os.path.join(self.path, file), allow_pickle=True)
            if reshape_to_2828: 
                new_npz = [] 
                for i in range(len(loaded_np_rep)):
                    x = np.reshape(loaded_np_rep[i], (28, 28, 1))
                    new_npz.append(x)
                loaded_np_rep = {
                        "label" : file.split('_')[-1].split('.')[0],
                        "data" : new_npz
                    }
            data.append(loaded_np_rep)
        if (append):
            self.data = self.data if self.data != None else [] + data
        else: self.data = data
        return self.data

    def load_data_csv_nums(self, limit = math.inf, append = True):
        with open(self.path, newline='', encoding='utf-8') as training_data: 
            reader = csv.reader(training_data, delimiter='\t')
            return_formatted_data = [] 
            counter = 0
            for row in reader:
                if counter >= limit: break 
                data = self.deserialize_numbers_data(row[0])
                return_formatted_data.append(
                    {
                        "label" : [int(i == data[0]) for i in range(10)],
                        "data" : data[1]
                    }
                )
                counter += 1
        if (append):
            self.data = self.data if self.data != None else [] + return_formatted_data
        else: self.data = return_formatted_data
        return self.data

    def custom_mapper(self, func):
        for cell in self.data:
            cell["data"] = list(map(func, cell["data"]))
        return self.data
    
    @staticmethod
    def fix_b64_padding(b64_coded_string): 
        return b64_coded_string + ('=' * (4 - len(b64_coded_string) % 4)) 
    
    @staticmethod
    def image_base64_decode(image_encoded) -> str: 
        image_encoded = DataLoader.fix_b64_padding(image_encoded)
        return base64.b64decode(image_encoded)
    
    @staticmethod
    def load_resize_image(image_decoded, resize_dims : tuple[int] = (28, 28)) -> np.ndarray: 
        image_data = Image.open(BytesIO(image_decoded)).convert('L')
        image_data = ImageOps.invert(image_data)        
        enhancer = ImageEnhance.Brightness(image_data)
        image_data = enhancer.enhance(50)
        if resize_dims != None: 
            image_data = image_data.resize(resize_dims)
        np_rep = np.array([np.array(image_data)]) 
        return  np_rep
    
    @staticmethod
    def b64_img_to_nparr(image_encoded): 
        return DataLoader.load_resize_image(DataLoader.image_base64_decode(image_encoded))
        
    @staticmethod        
    def interpolate(data : list): 
        return np.interp(data, [-1, 1], [0, 255])
    
    @staticmethod
    def numpy_array_mapper(numpy_array : np.ndarray, transformation_func): 
        vectorized_function = np.vectorize(transformation_func)
        return vectorized_function(numpy_array)

    @staticmethod
    def convert_arr_to_img(array): 
        new_arr = np.reshape(array, (28, 28))
        return Image.fromarray(new_arr)

    @staticmethod
    def visualize_array(array): 
        img = DataLoader.convert_arr_to_img(array)
        img.show(title="image_repo")
    
    @staticmethod
    def deserialize_numbers_data(row : str):
        number_label, *data = map( lambda x : float(x), row.split(','))
        return [number_label, data] 

    def set_labels(self, data, label): 
        pass 
        # TODO: after formatting training plan for doodles 
