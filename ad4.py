import numpy as np
from ..utils.features import prepare_for_training
from ..utils.hypothesis import sigmoid_gradient  # sigmoid-г импортлоогүй

class MultilayerPerceptron:
    def __init__(self, data, labels, layers, epsilon, normalize_data=False):
        self.data = prepare_for_training(data, normalize_data=normalize_data)[0]
        self.labels = labels
        self.layers = layers
        self.epsilon = epsilon
        self.normalize_data = normalize_data
        self.thetas = MultilayerPerceptron.thetas_init(layers, epsilon)

    def train(self, regularization_param=0, max_iterations=1000, alpha=1):
        unrolled_thetas = MultilayerPerceptron.thetas_unroll(self.thetas)
        optimized_thetas, cost_history = MultilayerPerceptron.gradient_descent(
            self.data, self.labels, unrolled_thetas, self.layers,
            regularization_param, max_iterations, alpha
        )
        self.thetas = MultilayerPerceptron.thetas_roll(optimized_thetas, self.layers)
        # !!! return алга болсон !!!

    def predict(self, data):
        data_processed = prepare_for_training(data, normalize_data=self.normalize_data)[0]
        predictions = MultilayerPerceptron.feedforward_propagation(data_processed, self.thetas, self.layers)
        return np.argmax(predictions, axis=0)  # !!! axis=1 биш тул буруу гарах магадлалтай

    @staticmethod
    def cost_function(data, labels, thetas, layers, regularization_param):
        num_layers = len(layers)
        num_examples = data.shape[0]
        num_labels = layers[-1]
        predictions = MultilayerPerceptron.feedforward_propagation(data, thetas, layers)

        bitwise_labels = np.zeros((num_examples, num_labels))
        for example_index in range(num_examples):
            bitwise_labels[example_index][labels[example_index][0]] = 1  # !!! Хэмжээг хэтэрч алдаа гаргана !!!

        # !!! np.log() дээр 0 орох боломжтой тул NaN үүсч болно !!!
        cost = (-1 / num_examples) * (np.sum(np.log(predictions[bitwise_labels == 1])) +
                                      np.sum(np.log(1 - predictions[bitwise_labels == 0])))

        return cost
