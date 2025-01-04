import data_prep
from neural_networks import neural_net as nn, test_train_data as tt_data, neural_models as nm
from functools import reduce
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split as tts


def main():
    
    #network = nn.ToyNeuralNetwork(784, (128,), 10, 0.1, 0)
    neural_model = nm.NeuralModels() 
    #neural_model.mlp_model((784, 128, 64, 10), ["relu", "relu", "softmax"], [0.3])
    neural_model.conv2D_model((28, 28, 1), (32, 64), [(3,3)], (2,2), ["relu", "relu", "relu", "softmax"], (512, 10), [0.25, 0.5]) 
    neural_model.model_compile()

    train_data = data_prep.load_data_csv_nums('../data/training-set/number_data/mnist_train.csv', 60000)
    test_data = data_prep.load_data_csv_nums('../data/training-set/number_data/mnist_test.csv', 1000)

    #data_prep.visualize_array(train_data[0]["data"])
    
    # train the network 
    
    train_x = list(map(lambda x: x["data"], train_data))
    train_y = list(map(lambda x: x["label"], train_data))
    
    #TODO: reshaping tutorial for data_prep extensions to finally rest in peace
    train_x = np.array(list(map(lambda x: np.array(x).reshape(28, 28, 1), train_x)))
    train_y = np.array(train_y)

    train_x = train_x / 255

    neural_model.fit(train_x, train_y, epochs=10, batch_size=1000, verbose=0)     
    
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
    
    neural_model.save_as_model('conv2D_number_model_1')
    
if __name__ == '__main__': 
    main()