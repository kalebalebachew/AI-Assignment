from flask import Flask, render_template, request, jsonify
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Load the pre-trained model and vectorizer
model = joblib.load('')
vectorizer = joblib.load('')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    notes = data['notes']

    # Preprocess the input notes
    notes_tfidf = vectorizer.transform([notes])

    # Make predictions
    prediction = model.predict(notes_tfidf)[0]

    return jsonify({'prediction': 'Related to Exam' if prediction == 1 else 'Not related to Exam'})

if __name__ == '__main__':
    app.run(debug=True)
