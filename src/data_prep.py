
import numpy as np
import os
from PIL import Image
import csv
import math

# 28*28 - image resolution, both for numbers and doodles   

class DataLoader:

    def __init__(self, path):
        self.path = path
        self.data = None

    def load_data_npy(self, dir : str, reshape_to_2828 : bool = False): 
        data = []
        files = [os.path.join(dir, file) for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]
        for file in files: 
            loaded_np_rep = np.load(file, allow_pickle=True)
            if reshape_to_2828: 
                new_npz = [] 
                for i in range(len(loaded_np_rep)):
                    x = np.reshape(loaded_np_rep[i], (28, 28))
                    x = np.expand_dims(x, axis=0)
                    x = np.reshape(loaded_np_rep[i], (28, 28, 1))
                    new_npz.append(x)
                loaded_np_rep = new_npz 
            data.append(loaded_np_rep)
        return data
    
    def interpolate(self,  data : list): 
        return np.interp(data, [-1, 1], [0, 255])

    def convert_arr_to_img(self, array): 
        new_arr = np.reshape(array, (28, 28))
        return Image.fromarray(new_arr)

    def visualize_array(self, array): 
        img = self.convert_arr_to_img(array)
        img.show(title="image_repo")

    def deserialize_numbers_data(self, row : str):
        number_label, *data = map( lambda x : float(x), row.split(','))
        return [number_label, data]    

    #TODO: create interface for data or atleast object to handle it better
    def load_data_csv_nums(self, limit = math.inf):
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
        self.data = return_formatted_data
        return return_formatted_data
    
    def custom_mapper(self, func):
        for cell in self.data:
            cell["data"] = list(map(func, cell["data"]))
        return self.data

    def set_labels(self, data, label): 
        pass 
        # TODO: after formatting training plan for doodles 
