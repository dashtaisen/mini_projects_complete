import random
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from nltk.corpus import movie_reviews as reviews
from sklearn.naive_bayes import GaussianNB

class Review:

    def __init__(self):
        #self.docs = [(list(reviews.words(fileid)), category) for category in reviews.categories() for fileid in reviews.fileids(category)]
        self.docs = [(reviews.raw(fileid), category) for category in reviews.categories() for fileid in reviews.fileids(category)]
        random.shuffle(self.docs)
        self.train_data = []
        self.train_labels = []
        self.test_data = []
        self.test_labels = []
        self.train_vectors = None
        self.test_vectors = None
        self.load_docs()
        self.vectorize_tfidf()

    def load_docs(self):
        for i in range(len(self.docs)):
            if i < len(self.docs) * .8:
                self.train_data.append(self.docs[i][0])
                self.train_labels.append(self.docs[i][1])
            else:
                self.test_data.append(self.docs[i][0])
                self.test_labels.append(self.docs[i][1])

    def vectorize_tfidf(self):
        vectorizer = TfidfVectorizer(min_df=5, max_df = .8, sublinear_tf = True, use_idf = True)
        self.train_vectors = vectorizer.fit_transform(self.train_data)
        self.test_vectors = vectorizer.transform(self.test_data)

    def classify_sgd(self):
        clf = SGDClassifier(loss="hinge", penalty="l2")
        clf.fit(self.train_vectors, self.train_labels)
        prediction = clf.predict(self.test_vectors)
        return prediction

    def classify_svc(self):
        clf = svm.LinearSVC()
        clf.fit(self.train_vectors, self.train_labels)
        prediction = clf.predict(self.test_vectors)
        return prediction

    def classify_nb(self):
        clf = GaussianNB()
        clf.fit(self.train_vectors.toarray(), self.train_labels.toarray())
        prediction = clf.predict(self.test_vectors.toarray())
        return prediction

    def report(self, prediction):
        print(classification_report(self.test_labels, prediction))
