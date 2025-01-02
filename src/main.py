import data_prep
from neural_networks import neural_net as nn, test_train_data as tt_data
from functools import reduce

def main():
    
    network = nn.ToyNeuralNetwork(784, 75, 10, 0.1, 0)

    train_data = data_prep.load_data_csv_nums('../data/training-set/number_data/mnist_train.csv', 10000)
    test_data = data_prep.load_data_csv_nums('../data/training-set/number_data/mnist_test.csv', 1000)
    
    #data_prep.visualize_array(train_data[0]["data"])
    
    # train 
    for row in train_data: 
        network.train(list(map(lambda x : x / 255, row["data"])), row["label"])

    err_count = 0
    
    for row in test_data: 
        output_list = network.predict(list(map(lambda x : x / 255, row["data"]))).reshape(1, -1).tolist()[0]
        # print(output_list)
        # print(reduce(lambda x, y: x + y, output_list, 0))
        # print("Based on model, the most likely is ", output_list.index(max(output_list)), " with percentage of ", (max(output_list)) * 100, "%")
        # data_prep.visualize_array(row["data"])
        # input("Enter to continue...")
        if output_list.index(max(output_list)) != row["label"].index(max(row["label"])): 
            err_count += 1
            
                        
    print((err_count / len(test_data)) * 100, "% wrong guesses")
    
if __name__ == '__main__': 
    main()