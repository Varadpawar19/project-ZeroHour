import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif

# Load the transformed dataset from the specified file path
df = pd.read_json(r"D:\vscode\SIH\transformed_dataset.json")

# Print columns to inspect the structure
print(df.columns)

# Handle missing values (imputation)
imputer = SimpleImputer(strategy="mean")  # You can change the strategy (mean, median, most_frequent, etc.)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Ensure Date is datetime type
df['Reported_Date'] = df['Reported_Date'].fillna('Not Specified')  # Fill missing reported date with a placeholder
df['Description'] = df['Description'].fillna('No description available')  # Fill missing description with a placeholder

# Handle 'Time' column (extract hour and minute)
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
df['Hour'] = df['Time'].dt.hour  # Extract hour
df['Minute'] = df['Time'].dt.minute  # Extract minute

# Feature extraction (e.g., extracting the length of Description)
df['description_length'] = df['Description'].apply(len)

# Binning 'Threat_Level' into numeric values (if it's categorical)
df['Threat_Level'] = df['Threat_Level'].map({'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4})

# Data Cleaning (remove duplicate incidents based on the Incident_ID)
df = df.drop_duplicates(subset='Incident_ID')

# Normalization and Standardization
scaler = MinMaxScaler()  # Normalization
df['description_length_normalized'] = scaler.fit_transform(df[['description_length']])

standard_scaler = StandardScaler()  # Standardization
df['description_length_standardized'] = standard_scaler.fit_transform(df[['description_length']])

# Encode categorical target variable 'Sector' (Label Encoding)
label_encoder = LabelEncoder()
df['Sector_encoded'] = label_encoder.fit_transform(df['Sector'])

# Feature Selection using SelectKBest (if you have multiple features)
X = df[['description_length', 'description_length_normalized', 'description_length_standardized', 'Hour', 'Minute', 'Threat_Level']]
y = df['Sector_encoded']  # Encoded target variable

selector = SelectKBest(score_func=f_classif, k='all')
X_new = selector.fit_transform(X, y)

# Regression (if you want to perform linear regression)
X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Print the selected feature names
selected_features = X.columns[selector.get_support()]
print(f"Selected Features: {selected_features}")

# Print model results
print(f"Model Coefficients: {regressor.coef_}")
print(f"Model Intercept: {regressor.intercept_}")

# Save the cleaned and preprocessed data to a new JSON file
df.to_json(r"cleaned_cybersecurity_data2.json", orient='records', lines=True)
