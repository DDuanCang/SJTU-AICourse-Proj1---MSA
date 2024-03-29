from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.datasets import fetch_openml
import numpy as np
import joblib

from scipy.io import loadmat


def load_mnist():
    '''
    output: x, y as numpy matrix, x and y type as np.uint8(0-255)
    '''
    mnist = fetch_openml("mnist_784", version=1,
                         as_frame=False, data_home='./datasets')
    x, y = fetch_openml("mnist_784", version=1,
                        return_X_y=True, as_frame=False)
    x, y = np.uint8(x), np.uint8(y)
    return x, y, mnist


# due to the bad network, use the local mnist-original.mat data
#mnist = fetch_openml("mnist_784",data_home='./datasets')
mnist = loadmat(
    'D:\\Git\\SJTU-AICourse-Proj1---MSA\\proj2\\MNIST_svm\\datasets\\mnist-original.mat')
mnist.keys()
print(mnist)

x = mnist['data']
y = mnist['label']
x = np.swapaxes(x, 0, 1)
print(x.shape)
print(x)
y = np.squeeze(y)
print(y.shape)
print(y)


shape = 'ovr'

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.08, train_size=0.4, random_state=4)
# parameters:
# X_train,X_test, y_train, y_test =sklearn.model_selection.train_test_split(train_data,train_target,test_size=0.4, random_state=0,stratify=y_train)
# train_data
# train_target
# test_size: float or int,default=None; if float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split.If int, represents the absolute number of test samples. If None, the value is set to the complement of the train size. If train_size is also None, it will be set to 0.25.
# train_size: float or int, default=None; If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the train split. If int, represents the absolute number of train samples. If None, the value is automatically set to the complement of the test size.
# random_state: int,RandomState instance or None,default=None; Controls the shuffling applied to the data before applying the split. Pass an int for reproducible output across multiple function calls.
# shuffle: bool,default=True; Whether or not to shuffle the data before splitting. If shuffle=False then stratify must be None.
# stratify: array-like,default=None;
# return: splitting: list, length=2*len(arrays)

"""
svm.attribute:
    svm.LinearSVC
    svm.LinearSVR
    svm.NuSVC
    svm.VuSVR
    svm.OneClassSVM
    svm.SVC
    svm.SVR
    svm.l1_min_c
"""
predictor = svm.SVC(gamma='scale', C=1,
                    decision_function_shape=shape, kernel='sigmoid')
# parameters:
# C: float,default=1.0; must be strictly positive
# kernel: 'linear','poly','rbf','sigmoid','precomputed',default='rbf'
# degree: int,default=3; degree of the poly nomial kernel function('poly'), ignored by other kernel
# gamma: {'scale','auto'} or float, default='scale'; kernel coefficient for 'rbf','poly' and 'sigmoid'
# coef0: float, default=0.0; independent term in kernel function, only significant in 'poly' and 'sigmoid'
# shrinking: bool,default=True; whether to use the shrinking heuristic
# probability: bool,default=False; whether to enable probability estimates. this must be enabled prior to calling fit, will slow down that method as it internally uses 5-fold cross-validation, and predict_proba may be inconsistent with predict.
# tol: float, default=1e-3; tolerance for stopping criterion
# cache_size:fit,default=200; specify the size of the kernel cache(in MB)
# class_weight: dict or 'balanced',default=None; Set the parameter C of class i to class_weight[i]*C for SVC. If not given, all classes are supposed to have weight one. The “balanced” mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y))
# verbose: bool,default=False; enable verbose output.
# max_iter: int,default=-1; hard limit on iterations within solver, or -1 for no limit
# decision_function_shape: {'ovo','ovr'},default='ovr';
# ovo: one versus one, it will build k*(k-1)/2 classifiers for k kinds
# ovr: one versus rest, it will build k classifiers for k kinds
# break_ties: bool,default=False; If true, decision_function_shape='ovr', and number of classes > 2, predict will break ties according to the confidence values of decision_function; otherwise the first class among the tied classes is returned.
# random_state: int,RandomState instance or None,default=None; Controls the pseudo random number generation for shuffling the data for probability estimates. Ignored when probability is False. Pass an int for reproducible output across multiple function calls.


predictor.fit(x_train, y_train)
# fit(X,y,sample_weight=None): fit the SVM model according to the given training data
# parameters:
# X:train data
# y:train data label
# sample_weight:weight of the training data
# return: self:object; fitted estimator


joblib.dump(predictor, 'svm.pkl')
# save trained model to local file .pkl

predictor = joblib.load('./svm.pkl')
# load .pkl model from local file

result = predictor.predict(x_test)
# predict(X): perform classification on samples in X; for an one-class model,+1 or -1 is returned
# parameters:
# X:{array-like, sparse matrix} of shape (n_samples, n_features) or (n_samples_test, n_samples_train)
# return: y_pred:ndarray of shape (n_samples,); Class labels for samples in X

print(result)
print(y_test)
print(predictor.score(x_test, y_test))


# for report data
'''
for temp in range(1, 11):
    print(temp)
    shape = 'ovo'

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.08, train_size=0.4, random_state=4)

    predictor = svm.SVC(gamma='scale', C=0.3*temp,
                        decision_function_shape=shape, kernel='rbf')

    predictor.fit(x_train, y_train)
    joblib.dump(predictor, 'svm.pkl')
    predictor = joblib.load('./svm.pkl')
    result = predictor.predict(x_test)

    print(predictor.score(x_test, y_test))
'''
