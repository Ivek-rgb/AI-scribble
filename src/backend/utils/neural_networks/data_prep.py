import os
import csv
import math
import base64
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
from collections.abc import Sized
<<<<<<< HEAD
from random import shuffle
=======
>>>>>>> 893b92634566a83dd5e99a9754553bf9bd932353

# 28*28 - image resolution, both for numbers and doodles   
# data loader class with handful of image and array manipulation functions   

class DataLoader:
    
    CATEGORIES_STORAGE_PATH = os.path.join(os.path.dirname(__file__), '../../data/') 

    def __init__(self, path):
        self.path = path
        self.past_paths = []
        self.categories = {}
        self.elements = None
        
    def set_new_path(self, new_path): 
        if self.path != None: self.past_paths.append(self.path)
        self.path = new_path
    
    def return_split_data_labels(self, transform_categories = False) -> tuple[np.ndarray, np.ndarray]:
        data, labels = (None, None)
        if not transform_categories:  
            data, labels = zip(*[(row["data"], row["label"]) for row in self.elements])
        else: 
            data, labels = zip(*[(row["data"], [int(self.categories[row["label"]] == idx) for idx in range(len(self.categories))]) for row in self.elements])
        return np.array(data), np.array(labels)
    
    @staticmethod
    def get_all_files_from_dir(dir_path:str, *supported_extensions :str) -> list[str]: 
        return DataLoader.get_files_from_dir(dir_path, math.inf, *supported_extensions)
    
    @staticmethod
<<<<<<< HEAD
    def get_files_from_dir(dir_path: str, limit: int, *supported_extensions : str, shuffle_files : bool = False) -> list[str]: 
        supported_extensions = set(supported_extensions)
        listed_elements = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file)) and os.path.splitext(file)[1] in supported_extensions]
        if shuffle_files : shuffle(listed_elements) 
        return listed_elements[:min(limit, len(listed_elements))]
=======
    def get_files_from_dir(dir_path: str, limit: int, *supported_extensions : str) -> list[str]: 
        supported_extensions = set(supported_extensions)
        listed_elements = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file)) and os.path.splitext(file)[1] in supported_extensions]
        fetched_files = listed_elements[:min(limit, len(listed_elements))] 
        return fetched_files
>>>>>>> 893b92634566a83dd5e99a9754553bf9bd932353
    
    @staticmethod
    def handle_reshaping_array(start_array, reshape_dims : tuple[int, int, int] | None = None) -> np.ndarray: 
        if reshape_dims: 
            return np.array(start_array).reshape(reshape_dims)
    
    @staticmethod
    def load_npy_array_from_file(file_path: str, limit_to_data : int = math.inf, reshape_dims: tuple[int, int, int] | None = None, allow_pickle = True) -> np.ndarray[np.ndarray]: 
        loaded_np_rep = np.load(file_path, allow_pickle=allow_pickle)
        loaded_np_rep = loaded_np_rep[:min(limit_to_data, len(loaded_np_rep))]        
        if reshape_dims != None: 
            loaded_np_rep = [DataLoader.handle_reshaping_array(array, reshape_dims) for array in loaded_np_rep] 
        return loaded_np_rep
    
    @staticmethod
    def fix_b64_padding(b64_coded_string): 
        return b64_coded_string + ('=' * (4 - len(b64_coded_string) % 4)) 
    
    @staticmethod
    def image_base64_decode(image_encoded) -> str: 
        image_encoded = DataLoader.fix_b64_padding(image_encoded)
        return base64.b64decode(image_encoded)
    
    @staticmethod
    def load_resize_image(image_decoded, resize_dims : tuple[int] = (28, 28), invert_colors = True) -> np.ndarray: 
        image_data = Image.open(BytesIO(image_decoded)).convert('L')
        if invert_colors: image_data = ImageOps.invert(image_data)        
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
        return Image.fromarray(np.reshape(array, (28, 28)))

    @staticmethod
    def visualize_array(array): 
        img = DataLoader.convert_arr_to_img(array)
        img.show(title="image_repo")
    
    @staticmethod
    def deserialize_numbers_data(row : str):
        number_label, *data = map( lambda x : float(x), row.split(','))
        return [number_label, data]
    
<<<<<<< HEAD
    
    def shuffle_elements(self):
        self.elements = shuffle(self.elements) 
    
    def load_data_npy_dir(self, categories_save_filename: str | None, limit_files: int = math.inf, limit_data: int = math.inf, reshape_to_2828 : bool = False, shuffle_files = False, append = True) -> list: 
        data = []
        files = self.get_files_from_dir(self.path, limit_files, ".npy", ".h5", shuffle_files=shuffle_files)
=======
    def load_data_npy_dir(self, categories_save_filename: str | None, limit_files: int = math.inf, limit_data: int = math.inf, reshape_to_2828 : bool = False, append = True) -> list: 
        data = []
        files = self.get_files_from_dir(self.path, limit_files, ".npy", ".h5")
>>>>>>> 893b92634566a83dd5e99a9754553bf9bd932353
        for file in files:
            loaded_np_rep = DataLoader.load_npy_array_from_file(os.path.join(self.path, file), limit_data, (28,28,1) if reshape_to_2828 else None)
            label_str = file.split('_')[-1].split('.')[0]
            for inner_matrix in loaded_np_rep: 
                data.append({
                    "label":label_str,
                    "data":inner_matrix
                })
            self.categories[str(label_str)] = 0
        if (append):
            self.elements = self.elements if self.elements != None else [] + data
        else: self.elements = data
        if categories_save_filename: 
            path = self.CATEGORIES_STORAGE_PATH + categories_save_filename + ".txt"
            with open(path, 'w+') as categories_file: 
                categories_file.write("\n".join(self.categories.keys()))
            self.load_categories(path) # refresh categories
        return self.elements


    def load_data_csv_nums(self, categories_save_filename: str | None, limit = math.inf, reshape_to_2828: bool = False,  append = True, custom_deserialization_func = deserialize_numbers_data, custom_hasing_func = lambda x: str(int(x))):
        with open(self.path, newline='', encoding='utf-8') as training_data: 
            reader = csv.reader(training_data, delimiter='\t')
            return_formatted_data = [] 
            categories = {}
            counter = 0
            category_count = 0            
            for row in reader:
                if counter >= limit: break 
                label_data = custom_deserialization_func(row[0])
                if reshape_to_2828: 
                    label_data[1] = DataLoader.handle_reshaping_array(label_data[1], (28, 28, 1))
                categories[custom_hasing_func(label_data[0])] = category_count
                return_formatted_data.append(
                    {
                        "label" : custom_hasing_func(label_data[0]),
                        "data" : label_data[1]
                    }
                )
                counter += 1
        if (append):
            self.elements = self.elements if self.elements != None else [] + return_formatted_data
        else: self.elements = return_formatted_data
        if categories_save_filename: 
            path = self.CATEGORIES_STORAGE_PATH + categories_save_filename + ".txt"
            with open(path, 'w+') as categories_file: 
                categories_file.write("\n".join(categories.keys()))
            self.load_categories(path) # refresh categories
        return self.elements
    
    def create_custom_element_generator(self, data_generate_function, label_generate_function, num_of_data : int, append: bool = True) -> list[np.ndarray]:

        generated_elements = [
            {"data": np.array(data_generate_function()), "label": label_generate_function()}
            for _ in range(num_of_data)
        ]

        if append:
            self.elements.extend(generated_elements)
        else: self.elements = generated_elements 

        return self.elements
    
    def load_categories(self, category_file_path, key_is_category_name = True) -> map: 
        ret_categories = DataLoader.load_categories_static(category_file_path, key_is_category_name)
        self.categories = ret_categories
        return ret_categories 
        
    @staticmethod
    def load_categories_static(category_file_path, key_is_category_name = True) -> map:
        ret_categories = {}
        with open(category_file_path, "r") as category_file: 
            categories = category_file.read().splitlines() 
            if key_is_category_name: 
                for idx, category in enumerate(categories): 
                    ret_categories[category] = idx
            else: 
                for idx, category in enumerate(categories): 
                    ret_categories[idx] = category
            return ret_categories
        
    
    def map_elements(self, data_mapper = lambda x : x, label_mapper = lambda x : x) -> list[np.ndarray]:
        for element in self.elements: 
            data, label = element["data"], element["label"]
            data = data_mapper(data)
            label = label_mapper(label)
            element["data"] = data
            element["label"] = label
        return self.elements

    def map_data(self, data_mapper = lambda x : x): 
        return self.map_elements(data_mapper=data_mapper)

    def map_labels(self, label_mapper = lambda x: x): 
        return self.map_elements(label_mapper=label_mapper)
        
    def filter_elements(self, data_filter=lambda x: True, label_filter=lambda x: True) -> list[dict]:
        filtered_elements = [
            element for element in self.elements
            if data_filter(element["data"]) and label_filter(element["label"])
        ]
        self.elements = filtered_elements
        return self.elements

    def filter_data(self, data_filter=lambda x: True) -> list[dict]:
        return self.filter_elements(data_filter=data_filter)

    def filter_labels(self, label_filter=lambda x: True) -> list[dict]:
        return self.filter_elements(label_filter=label_filter)

    def return_categories(self): 
        return self.categories.keys()
    
    def return_loaded_paths(self): 
        return self.past_paths