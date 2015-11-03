from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import featherweight_api


class Classifier(object):
    def __init__(self):
        self.iris = datasets.load_iris()
        X = self.iris.data
        y = self.iris.target
        self.clf = RandomForestClassifier()
        self.clf.fit(X, y)

    def score(self,
              sepal_length,
              sepal_width,
              petal_length,
              petal_width):
        guessed_class_arr = self.clf.predict([sepal_length, sepal_width, petal_length, petal_width])
        guessed_class = guessed_class_arr[0]  # extract the only item in the array result
        guessed_class_label = self.iris.target_names[guessed_class]
        # note that guessed_class is a np.int64 and
        # guess_class_label is a Python string, they both
        # come from numpy arrays
        return {'guessed_label': guessed_class_label,
                'guessed_class': guessed_class}

classifier = Classifier()
featherweight_api.register(classifier.score)
featherweight_api.run()  # serve on localhost:5000 by default

# the following call will identify as class 2 ('virginica')
# http://localhost:5000/score?sepal_length=5.9&sepal_width=3&petal_length=5.1&petal_width=1.8
