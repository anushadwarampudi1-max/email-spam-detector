import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle

# Sample training data
data = {
    "text": [
        "Congratulations! You have won a free prize. Click here to claim now.",
        "You have been selected for a cash reward of 50000. Claim immediately.",
        "URGENT! Your account has won a lottery prize. Send your details now.",
        "Get free money by clicking this special link.",
        "You are a lucky winner. Call this number to receive your prize.",
        "Limited time offer! Buy now and get 90 percent discount.",
        "You have won a free vacation. Click the link to claim.",
        "Your mobile number has won a cash prize. Contact us immediately.",
        "Earn money from home with no investment. Join now.",
        "Congratulations, you are selected for a free gift card.",
        "Hi, please find the meeting schedule attached.",
        "Can you send me the project report by tomorrow?",
        "Your assignment submission deadline is Friday.",
        "The meeting has been moved to 3 PM.",
        "Please review the document and send your feedback.",
        "Your interview is scheduled for Monday at 10 AM.",
        "Thank you for your email. We will get back to you soon.",
        "Please find the invoice attached for your reference.",
        "The class will start at 9 AM tomorrow.",
        "Can you please share the presentation with me?"
    ],
    "label": [
        "spam", "spam", "spam", "spam", "spam",
        "spam", "spam", "spam", "spam", "spam",
        "ham", "ham", "ham", "ham", "ham",
        "ham", "ham", "ham", "ham", "ham"
    ]
}

df = pd.DataFrame(data)

# Create the machine learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

# Train the model
model.fit(df["text"], df["label"])

# Save the trained model
with open("spam_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("AI spam detection model trained successfully!")
print("Model saved as spam_model.pkl")