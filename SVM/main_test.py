__author__ = 'Konrad Kopciuch'

from sklearn import datasets
from sklearn import svm
import pickle

iris = datasets.load_iris()
digits = datasets.load_digits()

clf = svm.SVC(gamma=0.001, C=100., probability=True)
clf.fit(digits.data[:-1], digits.target[:-1])
print clf.predict(digits.data[-1])

for index, prob in enumerate(clf.predict_proba(digits.data[-1])[0]):
    print index, prob


#s = pickle.dumps(clf)
