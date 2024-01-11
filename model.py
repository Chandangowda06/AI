from sklearn.linear_model import RidgeClassifier
from sklearn.semi_supervised import SelfTrainingClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import joblib
import os

def predict(text:list):
    # Load the dataset
    df = pd.read_csv('tweet_emotions.csv')

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(df.content, df.sentiment,
                                                        test_size=0.0007,
                                                        random_state=1, shuffle=True)

    # Vectorize and transform the training data
    X_CountVectorizer = CountVectorizer(stop_words='english')
    X_train_counts = X_CountVectorizer.fit_transform(X_train)
    X_TfidfTransformer = TfidfTransformer()
    X_train_tfidf = X_TfidfTransformer.fit_transform(X_train_counts)

    # Train a SelfTrainingClassifier with a RidgeClassifier
    clf = SelfTrainingClassifier(RidgeClassifier())
    clf.fit(X_train_tfidf, y_train)

    # Save the trained model
    model_filename = 'self_training_model.joblib'
    joblib.dump(clf, model_filename)

    # Save the CountVectorizer
    vectorizer_filename = 'count_vectorizer.joblib'
    joblib.dump(X_CountVectorizer, vectorizer_filename)

    # Later, you can load the model and vectorizer as follows:

    # Load the trained model
    loaded_model = joblib.load(model_filename)

    # Load the CountVectorizer
    loaded_vectorizer = joblib.load(vectorizer_filename)

   
    text_transformed = loaded_vectorizer.transform(text)

    # Predict sentiment using the loaded model
    prediction = loaded_model.predict(text_transformed)

    return prediction

