# AI-IDS-Project

# Using pandas to import the dataset
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report
import joblib

# Load dataset without assuming headers
df = pd.read_csv(r"C:\Users\Joshua Herrera\Downloads\UNSW-NB15.csv", low_memory=False, header=None)

# Define correct column names from the UNSW-NB15 documentation
col_names = [
    "srcip", "sport", "dstip", "dsport", "proto", "state", "dur", "sbytes", "dbytes", 
    "sttl", "dttl", "sloss", "dloss", "service", "Sload", "Dload", "Spkts", "Dpkts",
    "swin", "dwin", "stcpb", "dtcpb", "smeansz", "dmeansz", "trans_depth", "res_bdy_len", 
    "Sjit", "Djit", "Stime", "Ltime", "Sintpkt", "Dintpkt", "tcprtt", "synack", "ackdat", 
    "is_sm_ips_ports", "ct_state_ttl", "ct_flw_http_mthd", "is_ftp_login", "ct_ftp_cmd", 
    "ct_srv_src", "ct_srv_dst", "ct_dst_ltm", "ct_src_ltm", "ct_src_dport_ltm", 
    "ct_dst_sport_ltm", "ct_dst_src_ltm", "attack_cat", "label"
]

# Ensure the dataset has at least the required number of columns
if len(df.columns) >= len(col_names):
    df = df.iloc[:, :len(col_names)]  # Trim unnecessary columns
    df.columns = col_names  # Assign correct names
else:
    print(f"Warning: Expected {len(col_names)} columns but found {len(df.columns)}. Check dataset.")

# Drop unnecessary columns (IPs, Ports, attack_cat since it's mostly NaN)
df.drop(columns=["srcip", "dstip", "sport", "dsport", "attack_cat"], inplace=True)

# Convert categorical columns to numeric using Label Encoding
categorical_cols = ["proto", "state", "service"]
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])  # Convert categories to numbers
    label_encoders[col] = le  # Store encoders for future use

# Define Features (X) and Target Label (y)
X = df.drop(columns=["label"])  # All columns except "label"
y = df["label"]  # Target: 0 (Normal) or 1 (Attack)

# Scale the numeric features for better model performance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into Training and Testing Sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define the Random Forest model
rf = RandomForestClassifier(random_state=42)

# Define the hyperparameter grid for RandomizedSearchCV
param_dist = {
    'n_estimators': [50, 100, 200, 300],  # Number of trees in the forest
    'max_depth': [10, 20, 30, None],  # Max depth of each tree
    'min_samples_split': [2, 5, 10],  # Minimum samples to split an internal node
    'min_samples_leaf': [1, 2, 4],  # Minimum samples at leaf nodes
    'bootstrap': [True, False]  # Whether to use bootstrap sampling
}

# Set up RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_dist,
    n_iter=20,  # Number of random combinations to try
    cv=3,  # 3-fold cross-validation
    verbose=2,
    random_state=42,
    n_jobs=-1  # Use all available CPU cores
)

# Fit the model
print("\nRunning RandomizedSearchCV to optimize hyperparameters...")
random_search.fit(X_train, y_train)

# Best model after RandomizedSearchCV
best_model = random_search.best_estimator_

# Evaluate the best model on the test set
y_pred = best_model.predict(X_test)

# Print performance metrics
print("\nBest Model Performance on Test Set:")
print(classification_report(y_test, y_pred))

# Print best hyperparameters found by RandomizedSearchCV
print("\nBest Parameters Found:")
print(random_search.best_params_)

# Save the trained model
joblib.dump(best_model, "rf_ids_model.pkl")

# Save the scaler
joblib.dump(scaler, "scaler.pkl")

# Save encoders if needed later
joblib.dump(label_encoders, "label_encoders.pkl")

print("\n✅ Model, scaler, and encoders saved successfully!")
