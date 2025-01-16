from utils.neural_networks.data_prep import DataLoader
from utils.neural_networks.neural_models import NeuralModels
from functools import reduce
import numpy as np
import json 
import re
import ast

import tkinter
from PIL import ImageTk, Image 
import numpy as np
from utils.image_scroller import ImageScroller

def custom_letter_deserialize(row: str): 
    [letter, *rest] = map(lambda x: float(x), row.split(','))
    letter = chr(ord('a') + int(letter) - 1)
    return [letter, rest]

def main():
    ImageScroller()

    data_test_loader = DataLoader('../../data/training-set/doodles_data/')
    data_test_loader.load_data_npy_dir(None, 10, 5, True)
    
    data, labels = data_test_loader.return_split_data_labels(False)
    
    print(len(data_test_loader.categories))

    return 
    neural_model.change_model_name("conv2d_emnist_letters_augmented_1")
    
    train_data_loader = DataLoader('../../data/training-set/letters_data/emnist-letters-train.csv')
    
    train_data_loader.load_data_csv_nums(neural_model.model_name_tag, limit=20, reshape_to_2828=True, custom_deserialization_func=custom_letter_deserialize, custom_hasing_func=lambda x: x)
    
    train_x, train_y = train_data_loader.return_split_data_labels(True)
    DataLoader.visualize_array(train_x[0])
    
    return 
    
    train_data_loader.map_data(lambda x: x / 255)

    train_x, train_y = train_data_loader.return_split_data_labels(True)

    neural_model.conv2D_model((28, 28, 1), (16, 32, 64), [(6,6), (5,5)], (2,2), ["relu", "relu", "relu", "relu", "relu", "softmax"], (256, 512, len(train_data_loader.categories)), [0.25, 0.25]) 
    neural_model.set_augmentation_datagen(width_shift=0, height_shift=0, rotation_level_deg=5)
    neural_model.model_compile()
    
    neural_model.fit(train_x, train_y, epochs=20, batch_size=1000, verbose=1)  
    neural_model.save_model('./models/')  
                
    return 
    new_data_loader = DataLoader('../../data/training-set/number_data/mnist_train.csv')
    test_data_loader = DataLoader('../../data/training-set/number_data/mnist_test.csv') 

    neural_model = NeuralModels() 
    neural_model.change_model_name("mnist_trained_model_1")
    
    new_data_loader.load_data_csv_nums('rand_save_file', 20, reshape_to_2828=True)
    test_data_loader.load_data_csv_nums(None, reshape_to_2828=True)

    #new_data_loader.map_elements(lambda x: x / 255, lambda x: [int(new_data_loader.categories[x] == idx) for idx in range(len(new_data_loader.categories))])
    #test_data_loader.map_elements(lambda x: x / 255, lambda x: [int(new_data_loader.categories[x] == idx) for idx in range(len(new_data_loader.categories))])
    
    train_x, train_y = new_data_loader.return_split_data_labels(True)  
    print(train_y[0])
    
    return 
    test_x, test_y = test_data_loader.return_split_data_labels() 
    
    neural_model.conv2D_model((28, 28, 1), (16, 32, 64), [(6,6), (5,5)], (2,2), ["relu", "relu", "relu", "relu", "relu", "softmax"], (256, 512, 10), [0.25, 0.25]) 
    neural_model.set_augmentation_datagen(width_shift=0.2, height_shift=0.2, rotation_level_deg=20)
    neural_model.model_compile()
    
    neural_model.fit(train_x, train_y, batch_size=200, epochs=20, verbose=1)
        
    loss, accuracy = neural_model.evaluate_model(test_x, test_y)
    print(loss, accuracy)
    neural_model.save_as_model('./models/', 'conv2D_mnist_low_training_augmented')
    
if __name__ == '__main__': 
    main()