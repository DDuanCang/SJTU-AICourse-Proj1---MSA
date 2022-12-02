'''
    fetch MNIST dataset by using sklearn.datasets
    show the MNIST dataset
'''

# import dependent modules
from sklearn.datasets import fetch_openml
import numpy as np

def load_mnist():
    '''
    output: x, y as numpy matrix, x and y type as np.uint8(0-255)
    '''
    x, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    x, y = np.uint8(x), np.uint8(y)
    return x, y