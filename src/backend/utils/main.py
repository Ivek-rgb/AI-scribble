from data_prep import DataLoader
#from neural_networks import neural_net as nn, neural_models as nm
from functools import reduce
import numpy as np


def main():
    
    new_data_loader = DataLoader('../../../data/training-set/number_data/mnist_train.csv')
    
    new_data_loader.load_data_csv_nums('new_number_data', 20, True)
    
    data, labels = new_data_loader.return_split_labels_data()  
    
    DataLoader.visualize_array(data[7])
    
    return 
    neural_model = nm.NeuralModels() 

    pngs_loader = DataLoader('../../../data/training-set/doodles_data/')  
    pngs_loader.load_data_npy("categories", True, True) # loads images 
    
    [print(data["label"]) for data in pngs_loader.data] #unmixed pure batch data 
    
    return 
    #neural_model.mlp_model((784, 128, 64, 10), ["relu", "relu", "softmax"], [0.3])

    neural_model.conv2D_model((28, 28, 1), (16, 32, 64), [(6,6), (5,5)], (2,2), ["relu", "relu", "relu", "softmax"], (512, 10), [0.25, 0.5]) 
    neural_model.set_augmentation_datagen(5, 0, 0, 0, [0.5, 1]) # augmentator only rotates images slightly and zooms in on some 
    neural_model.model_compile()

    loader_train = data_prep.DataLoader('../../../data/training-set/number_data/mnist_train.csv') 
    
    
    return     
    loader_train.load_data_csv_nums()
    loader_test.load_data_csv_nums()
    #test_data = loader.load_data_csv_nums('../data/training-set/number_data/mnist_test.csv', 1000)
    
    #print("prije")
    train_data = loader_train.custom_mapper(lambda x: x / 255)
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

    neural_model.fit(train_x, train_y, epochs=100, batch_size=128, verbose=1) 
    print("Training completed")    
    
    #for row in train_data:
        #network.train(list(map(lambda x : x / 255, row["data"])), row["label"])

    err_count = 0
    
    for row in test_data:
        row_data = np.array(row["data"]).reshape(-1, 28, 28, 1)
        output_list = neural_model.predict(row_data, verbose=0).tolist()[0]
        #output_list = network.predict(list(map(lambda x : x / 255, row["data"]))).reshape(1, -1).tolist()[0]
        err_count += output_list.index(max(output_list)) != row["label"].index(max(row["label"]))
                        
    print((err_count / len(loader_test.data)) * 100, "% wrong guesses")
    
    neural_model.save_as_model('../models/', 'conv2D_number_model_1')
    
if __name__ == '__main__': 
    main()