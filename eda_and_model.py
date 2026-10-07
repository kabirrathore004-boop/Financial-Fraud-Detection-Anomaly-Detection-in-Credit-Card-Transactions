"""EDA + optional Isolation Forest baseline for credit-card fraud.
Run: python python/eda_and_model.py   (expects data/cc_data.csv)
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder

df = pd.read_csv("data/cc_data.csv")
df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])

# 1. Overview
print("Shape:", df.shape)
print("\nMissing values:\n", df.isnull().sum())
print("\nUnique values (categorical):\n", df.select_dtypes("object").nunique())
print("\nSummary stats:\n", df[["amt", "city_pop"]].describe())
print("\nTarget distribution:\n", df["is_fraud"].value_counts())

# 2. Outliers (IQR)
for col in ["amt", "city_pop"]:
    q1, q3 = df[col].quantile([.25, .75])
    iqr = q3 - q1
    n = ((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).sum()
    print(f"IQR outliers in {col}: {n}")

# 3. Visualisations
plt.figure(figsize=(15, 10))
plt.subplot(2, 3, 1); sns.histplot(df["amt"], bins=50, kde=True); plt.title("Amount distribution")
plt.subplot(2, 3, 2); sns.boxplot(x="is_fraud", y="amt", data=df); plt.title("Amount by fraud status")
plt.subplot(2, 3, 3); sns.countplot(x="category", data=df); plt.xticks(rotation=45); plt.title("Transactions by category")
plt.subplot(2, 3, 4); sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm"); plt.title("Correlation matrix")
plt.subplot(2, 3, 5); sns.scatterplot(x="city_pop", y="amt", hue="is_fraud", data=df.sample(20000, random_state=42)); plt.title("city_pop vs amt")
plt.subplot(2, 3, 6); df["is_fraud"].value_counts().plot(kind="pie", autopct="%1.2f%%"); plt.title("Fraud share")
plt.tight_layout(); plt.savefig("images/eda_overview.png", dpi=150)

# 4. Baseline anomaly detection (unsupervised, for demonstration)
X = df.drop(columns=["is_fraud", "trans_num", "cc_num", "first", "last", "street", "dob",
                     "trans_date_trans_time"], errors="ignore")
for col in X.select_dtypes("object").columns:
    X[col] = LabelEncoder().fit_transform(X[col])
X = StandardScaler().fit_transform(X)

contamination = df["is_fraud"].mean()          # ~0.0058
model = IsolationForest(contamination=contamination, random_state=42).fit(X)
flagged = model.predict(X) == -1
print("Flagged as anomalous:", flagged.sum())
print("Of which truly fraud:", int(df.loc[flagged, "is_fraud"].sum()), "/", int(df["is_fraud"].sum()))
