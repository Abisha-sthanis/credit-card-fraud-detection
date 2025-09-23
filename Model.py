import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
credit = pd.read_csv("E:/project 2/credit_card_fraud_dataset.csv")

# Encode categorical features
encod = LabelEncoder()
credit['TransactionType'] = encod.fit_transform(credit['TransactionType'])
credit['Location'] = encod.fit_transform(credit['Location'])

# Convert TransactionDate to datetime
credit['TransactionDate'] = pd.to_datetime(credit['TransactionDate'])

# Extract date & time features
credit['Year'] = credit['TransactionDate'].dt.year
credit['Month'] = credit['TransactionDate'].dt.month
credit['Day'] = credit['TransactionDate'].dt.day
credit['Hour'] = credit['TransactionDate'].dt.hour
credit['Minute'] = credit['TransactionDate'].dt.minute
credit['Second'] = credit['TransactionDate'].dt.second

# Drop original TransactionDate
X = credit.drop(['TransactionDate', 'IsFraud'], axis=1)
y = credit['IsFraud']

# Split dataset (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.70, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000)  # added max_iter for stability
model.fit(X_train_scaled, y_train)

# Check accuracy
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")

# Save model and scaler using pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("Model and scaler saved successfully!")
