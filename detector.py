import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("Loading CSV...")

train = pd.read_csv("scam-dialogue_train.csv")

texts = train["dialogue"].astype(str).tolist()
labels = train["label"].tolist()

print("Training model...")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

print("Model ready.")


def detect_scam(text):
    X_test = vectorizer.transform([text])
    pred = model.predict(X_test)[0]
    return True if pred == 1 else False


if __name__ == "__main__":
    print(detect_scam("Your bank account blocked today"))
    print(detect_scam("Hello how are you"))



