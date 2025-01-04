import data_prep
from neural_networks import neural_net as nn, test_train_data as tt_data, neural_models as nm
from functools import reduce
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split as tts


def main():
    
    #network = nn.ToyNeuralNetwork(784, (128,), 10, 0.1, 0)
    neural_model = nm.NeuralModels()
    neural_model.load_model('conv2D_number_model_1')
    test_data = data_prep.load_data_csv_nums('../data/training-set/number_data/mnist_test.csv', 1000)
    # train the network 
        
    #TODO: reshaping tutorial for data_prep extensions to finally rest in peace
    
    #for row in train_data:
        #network.train(list(map(lambda x : x / 255, row["data"])), row["label"])

    err_count = 0
    
    # do not forget to expand dims for prediction gamer 
    for row in test_data:
        row_data = row["data"]
        row_data = np.array(row_data).reshape(-1, 28, 28, 1)
        output_list = neural_model.predict(row_data, verbose=0).tolist()[0]
        #output_list = network.predict(list(map(lambda x : x / 255, row["data"]))).reshape(1, -1).tolist()[0]
        if output_list.index(max(output_list)) != row["label"].index(max(row["label"])): 
            err_count += 1
                                    
    print((err_count / len(test_data)) * 100, "% wrong guesses")

    
if __name__ == '__main__': 
    main()