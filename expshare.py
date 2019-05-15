import numpy as np
import sys
import pickle
import os
import neuralnetworks_pytorch as nn
import picturegenerator as pg


def percent_correct(actual, predicted):
    return 100 * np.mean(actual == predicted)


if __name__ == "__main__":
    # Read In Input
    if len(sys.argv) < 2:
        print("Wrong Number of Arguments. Requires 1 arg, the number of iterations to train. Must be more than 1000")
        sys.exit()
    neural_net_file = "trainednet.pkl"
    num_iterations = int(sys.argv[1]) // 10
    if num_iterations < 10:
        print("Wrong Number of Arguments. Requires 1 arg, the number of iterations to train. Must be more than 1000")
        sys.exit()

    # Load Network
    if os.path.isfile(neural_net_file):
        print('Loading Network From: ', neural_net_file)
        nnet = pickle.load(open(neural_net_file, "rb"))
        total_number_of_iterations = pickle.load(open("numits.pkl", "rb"))
        total_number_of_iterations = total_number_of_iterations + int(sys.argv[1])
    else:
        print('Creating Neural Network')
        channels = 4
        hiddenLayers = [20, 20, 20, 20, 20]
        outputs = 4  # So We Are Guessing The Last 2 Bits Of The Keys
        nnet = nn.NeuralNetworkClassifier_Pytorch(channels, hiddenLayers, outputs, n_conv_layers=4,
                                                  windows=[2, 2, 2, 2], strides=[1, 1, 1, 1],
                                                  input_height_width=32, gpu=True)
        total_number_of_iterations = int(sys.argv[1])

    for i in range(10):
        # Generate Data
        picgen = pg.PictureGenerator()
        pg.generate_pictures("trainingdata.npz", num_iterations)
        pg.generate_pictures("testingdata" + str(i) + ".npz", num_iterations // 10)

        # Load Data
        npz_file = np.load('trainingdata.npz')
        Xtrain = npz_file['data']
        Ttrain = npz_file['answers']
        npz_file = np.load('testingdata' + str(i) + '.npz')
        Xtest = npz_file['data']
        Ttest = npz_file['answers']

        # Train
        # print(Xtrain, Ttrain, Xtest, Ttest)
        nnet.train(Xtrain, Ttrain, Xtest, Ttest, 5, 100, 0.001)
        classes, probs, y = nnet.use(Xtest)
        print("Final Run Of Testing Data: " + str(percent_correct(Ttest, classes)))

    # Save Network
    pickle.dump(nnet, open("trainednet.pkl", "wb"))
    pickle.dump(total_number_of_iterations, open("numits.pkl", "wb"))
    os.remove("trainingdata.npz")
