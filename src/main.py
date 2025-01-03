import data_prep
from neural_networks import neural_net as nn, test_train_data as tt_data

def main():
    
    network = nn.ToyNeuralNetwork(784, 74, 10)

    train_data = data_prep.load_data_csv_nums('../data/training-set/number_data/mnist_train.csv', 7000)
    test_data = data_prep.load_data_csv_nums('../data/training-set/number_data/mnist_train.csv', 1000)
    
    #data_prep.visualize_array(train_data[0]["data"])
    
    # train 
    for row in train_data: 
        network.train(list(map(lambda x : x / 255, row["data"])), row["label"])

    test_data_fives = list(filter(lambda x : x["label"][5], test_data))
    
    err_count = 0
    
    for row in test_data_fives: 
        output_list = network.predict(list(map(lambda x : x / 255, row["data"]))).tolist()
        if output_list.index(max(output_list)) != row["label"].index(max(row["label"])): 
            err_count += 1
                        
    print((err_count / len(test_data_fives)) * 100, "% wrong guesses")
    network.save_model()
        
    
if __name__ == '__main__': 
    main()