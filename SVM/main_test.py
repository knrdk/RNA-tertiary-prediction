__author__ = 'Konrad Kopciuch'

from sklearn import datasets
from sklearn import svm
import pickle

iris = datasets.load_iris()
digits = datasets.load_digits()

print digits.data[1]
print digits.target[1]

clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-1], digits.target[:-1])
print clf.predict(digits.data[-1])

#s = pickle.dumps(clf)
