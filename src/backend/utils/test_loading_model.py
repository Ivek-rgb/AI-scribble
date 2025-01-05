import data_prep
from neural_networks import neural_net as nn, neural_models as nm
from functools import reduce
import numpy as np
import tensorflow as tf


def main():
    
    #network = nn.ToyNeuralNetwork(784, (128,), 10, 0.1, 0)
    neural_model = nm.NeuralModels() 
    #neural_model.mlp_model((784, 128, 64, 10), ["relu", "relu", "softmax"], [0.3])
    #neural_model.conv2D_model((28, 28, 1), (32, 64), [(3,3)], (2,2), ["relu", "relu", "relu", "softmax"], (512, 10), [0.25, 0.5]) 
    #neural_model.model_compile()

    neural_model.load_model('../models/conv2D_number_model_1.keras') 
    print(neural_model.model_name_tag)

    loader_test = data_prep.DataLoader('../../../data/training-set/number_data/mnist_test.csv') 

    loader_test.load_data_csv_nums(1000)
    #test_data = loader.load_data_csv_nums('../data/training-set/number_data/mnist_test.csv', 1000)
    
    #print("prije")
    test_data = loader_test.custom_mapper(lambda x: x / 255)
        
    #print("posli")
    #print(test_data[0])

    #loader.visualize_array(train_data[0]["data"])

    err_count = 0
    
    for row in test_data:
        row_data = row["data"]
        row_data = np.array(row_data).reshape(-1, 28, 28, 1)
        output_list = neural_model.predict(row_data, verbose=0).tolist()[0]
        #output_list = network.predict(list(map(lambda x : x / 255, row["data"]))).reshape(1, -1).tolist()[0]
        if output_list.index(max(output_list)) != row["label"].index(max(row["label"])): 
            err_count += 1
                        
    print((err_count / len(loader_test.data)) * 100, "% wrong guesses")
    
if __name__ == '__main__': 
    main()