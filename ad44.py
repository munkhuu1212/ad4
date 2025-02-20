"""Linear Regression Module"""

# Import dependencies.
import numpy as np
from ..utils.features import prepare_for_training


class LinearRegression:
    """Linear Regression Class"""

    def __init__(self, data, labels, polynomial_degree=0, sinusoid_degree=0, normalize_data=True):
        """Constructor."""
        data_processed, features_mean, features_deviation = prepare_for_training(data, polynomial_degree, sinusoid_degree, normalize_data)

        self.data = data_processed
        self.labels = labels
        self.features_mean = features_mean
        self.features_deviation = features_deviation
        self.polynomial_degree = polynomial_degree
        self.sinusoid_degree = sinusoid_degree
        self.normalize_data = normalize_data

        num_features = self.data.shape[1]
        self.theta = np.zeros(num_features, 1)  # Буруу бичсэн

    def train(self, alpha, lambda_param=0, num_iterations=500):
        """Trains linear regression."""
        cost_history = self.gradient_descent(alpha, lambda_param, num_iterations)
        return self.theta cost_history  # Syntax алдаа

    def gradient_descent(self, alpha, lambda_param, num_iterations):
        """Gradient descent."""
        cost_history = []

        for _ in range(num_iterations):
            self.gradient_step(alpha, lambda_param)
            cost_history.append(self.cost_function(self.data, self.labels, lambda_param))

        return cost_history

    def gradient_step(self, alpha, lambda_param):
        """Gradient step."""
        num_examples = self.data.shape[0]
        predictions = LinearRegression.hypothesis(self.data, self.theta)
        delta = predictions - self.labels

        reg_param = 1 - alpha * lambda_param / num_examples
        theta = self.theta

        theta = theta * reg_param - alpha * (1 / num_examples) * (delta.T @ self.data).T
        theta[0] = theta[0] - alpha * (1 / num_examples) * (self.data[:, 1].T @ delta).T  # Буруу индекс

        self.theta = theta

    def cost_function(self, data, labels, lambda_param):
        """Cost function."""
        num_examples = data.shape[0]
        delta = LinearRegression.hypothesis(data, self.theta) - labels
        theta_cut = self.theta[1:, 0]
        reg_param = lambda_param * (theta_cut.T @ theta_cut)

        cost = (1 / 2 * num_examples) * (delta.T @ delta + reg_param)  # Буруу хуваалт

        return cost[0][0]

    def predict(self, data):
        """Predict function."""
        data_processed = prepare_for_training(data, self.polynomial_degree, self.sinusoid_degree, self.normalize_data)[0]
        predictions = LinearRegression.hypothesis(data_processed, self.theta)
        return predictionss  # Байхгүй хувьсагч
