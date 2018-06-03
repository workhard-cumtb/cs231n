from __future__ import print_function
import numpy as np
import matplotlib.pyplot as pyplt

class TwoLayerNet(object):
    
    def __init__(self, input_size, hidden_size, output_size, std=1e-4):
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = std * np.zeros(hidden_size)
        self.params['W2'] = std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = std * np.zeros(output_size)
        
    def loss(self, X, y=None, reg=0.0):
        loss = 0.0
        grads = {}
        
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        N = X.shape[0]

        layer1_out = X.dot(W1) + b1
        relu_out = np.maximum(0, layer1_out)
        scores = relu_out.dot(W2) + b2
        
        if y is None:
            return scores

        stable_scores = scores - np.max(scores, axis=1, keepdims=True)
        correct_score = stable_scores[np.arange(N), y]

        loss = -np.sum(np.log(np.exp(correct_score) / np.sum(np.exp(stable_scores), axis=1)))
        loss = loss/N + reg * np.sum(W1 * W1) + reg * np.sum(W2 * W2)

        Dscores = np.exp(stable_scores) / np.sum(np.exp(stable_scores), axis=1, keepdims=True)
        Dscores[np.arange(N), y] -= 1
        Dscores = Dscores / N
        
        grads['b2'] = np.sum(Dscores, axis=0)
        grads['W2'] = relu_out.T.dot(Dscores) + 2 * reg * W2

        Drelu_out = Dscores.dot(W2.T)
        Dlayer1_out = Drelu_out * (layer1_out > 0)
        grads['b1'] = np.sum(Dlayer1_out, axis=0)
        grads['W1'] = X.T.dot(Dlayer1_out) + 2 * reg * W1  
        
        return loss, grads
        