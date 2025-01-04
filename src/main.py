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

    npy_loader = data_prep.DataLoader('../data/training-set/doodles_data/')
    
    loaded_data = npy_loader.load_data_npy('../data/training-set/doodles_data/', True) # resizeamo na 28, 28, 1 zbog korištenja konvolucijske mreže  

    print(len(loaded_data)) # broj dataseta odnosno kategorija crteža (jabuka, lav), koliko .npy fileova imaš 
    print(len(loaded_data[0])) # broj primjeraka unutar dataseta za jednu kategoriju crteža (jabuka, lav), koliko primjera crteža ima za prvu kategoriju 
    loaded_data = np.array(loaded_data)
    
    return # ovo kasnije je za brojeve pa ću samo to omittat preko return-a 

    loader_train = data_prep.DataLoader('../data/training-set/number_data/mnist_train.csv') 
    loader_test = data_prep.DataLoader('../data/training-set/number_data/mnist_test.csv') 
    
    loader_train.load_data_csv_nums(15000)
    loader_test.load_data_csv_nums(1000)
    #test_data = loader.load_data_csv_nums('../data/training-set/number_data/mnist_test.csv', 1000)
    
    #print("prije")
    train_data = loader_train.custom_mapper(lambda x : x / 255)
    test_data = loader_test.custom_mapper(lambda x: x / 255)
        
    #print("posli")
    #print(test_data[0])

    #loader.visualize_array(train_data[0]["data"])
    
    # train the network 
    
    train_x = list(map(lambda x: x["data"], train_data))
    train_y = list(map(lambda x: x["label"], train_data))
    
    #TODO: reshaping tutorial for data_prep extensions
    train_x = np.array(list(map(lambda x: np.array(x).reshape(28, 28, 1), train_x)))
    train_y = np.array(train_y)

    neural_model.fit(train_x, train_y, epochs=10, batch_size=1000, verbose=0)     
    
    #for row in train_data:
        #network.train(list(map(lambda x : x / 255, row["data"])), row["label"])

    err_count = 0
    
    for row in test_data:
        row_data = row["data"]
        row_data = np.array(row_data).reshape(-1, 28, 28, 1)
        output_list = neural_model.predict(row_data, verbose=0).tolist()[0]
        #output_list = network.predict(list(map(lambda x : x / 255, row["data"]))).reshape(1, -1).tolist()[0]
        if output_list.index(max(output_list)) != row["label"].index(max(row["label"])): 
            err_count += 1
                        
    print((err_count / len(loader_test.data)) * 100, "% wrong guesses")
    
    neural_model.save_as_model('./models/', 'conv2D_number_model_1')
    
if __name__ == '__main__': 
    main()