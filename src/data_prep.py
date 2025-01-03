
import numpy as np
import os
from PIL import Image
import csv
import math

# 28*28 - image resolution, both for numbers and doodles   

def load_data_npy(dir : str, reshape_to_2828 : bool = False): 
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
 
def interpolate( data : list): 
    return np.interp(data, [-1, 1], [0, 255])

def convert_arr_to_img(array): 
    new_arr = np.reshape(array, (28, 28))
    return Image.fromarray(new_arr)

def visualize_array(array): 
    img = convert_arr_to_img(array)
    img.show(title="image_repo")

def deserialize_numbers_data(row : str):
    number_label, *data = map( lambda x : float(x), row.split(','))
    return [number_label, data]    

#TODO: create interface for data or atleast object to handle it better
def load_data_csv_nums(dir : str, limit = math.inf):
    with open(dir, newline='', encoding='utf-8') as training_data: 
        reader = csv.reader(training_data, delimiter='\t')
        return_formatted_data = [] 
        counter = 0
        for row in reader:
            if counter >= limit: break 
            num_data =  deserialize_numbers_data(row[0])
            return_formatted_data.append(
                {
                    "label" : [int(i == num_data[0]) for i in range(10)],
                    "data" : num_data[1]
                }
            )
            counter += 1
    return return_formatted_data
    
def set_labels(data, label): 
    pass 
    # TODO: after formatting training plan for doodles 
