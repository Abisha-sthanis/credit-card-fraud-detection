from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load saved model and scaler
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# LabelEncoders for categorical features
transaction_type_encoder = LabelEncoder()
transaction_type_encoder.classes_ = np.array(['Purchase', 'Refund', 'Transfer', 'Withdrawal'])

location_encoder = LabelEncoder()
location_encoder.classes_ = np.array(['San Antonio', 'New York', 'Chicago'])

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form

        # Encode TransactionType and Location
        trans_type = transaction_type_encoder.transform([data['type']])[0]
        loc = location_encoder.transform([data['location']])[0]

        # Parse Transaction Date & Time
        transaction_datetime = pd.to_datetime(data['transaction_datetime'])

        # Extract Year, Month, Day, Hour, Minute, Second
        year = transaction_datetime.year
        month = transaction_datetime.month
        day = transaction_datetime.day
        hour = transaction_datetime.hour
        minute = transaction_datetime.minute
        second = transaction_datetime.second

        # Build input DataFrame
        input_data = pd.DataFrame([{
            'TransactionID': int(data['transaction_id']),
            'Amount': float(data['amount']),
            'MerchantID': int(data['merchant']),
            'TransactionType': trans_type,
            'Location': loc,
            'Year': year,
            'Month': month,
            'Day': day,
            'Hour': hour,
            'Minute': minute,
            'Second': second
        }])

        # Scale the input
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_scaled)[0]

        # Map result: 0 = Yes (Fraud), 1 = No (Not Fraud)
        result = "Yes (Fraud)" if prediction == 0 else "No (Not Fraud)"

        return render_template('output.html', result=result)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
