import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest


def detect_anomalies_zscore(data_path="data/bizpulse_data.csv", output_path="output/revenue_anomalies.csv"):
    df = pd.read_csv(data_path, parse_dates=['Date'])

    # Z-score anomaly detection on Revenue
    df['Revenue_Z'] = (df['Revenue'] - df['Revenue'].mean()) / df['Revenue'].std()
    df['Is_Anomaly_Z'] = df['Revenue_Z'].apply(lambda x: abs(x) > 3)

    # Save anomalies
    anomalies = df[df['Is_Anomaly_Z'] == True]
    anomalies.to_csv(output_path, index=False)

    # Plot anomalies
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Date', y='Revenue', label='Revenue')
    plt.scatter(anomalies['Date'], anomalies['Revenue'], color='red', label='Z-score Anomalies')
    plt.title("Z-score Revenue Anomalies")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/zscore_anomaly_plot.png")
    plt.close()
    print("✅ Z-score anomalies saved and plotted.")


def detect_anomalies_iforest(data_path="data/bizpulse_data.csv", output_path="output/iforest_anomalies.csv"):
    df = pd.read_csv(data_path, parse_dates=['Date'])

    # Select relevant features
    features = df[['Revenue', 'Profit', 'Marketing_Spend', 'Customer_Satisfaction']]
    model = IsolationForest(contamination=0.03, random_state=42)
    df['Is_Anomaly_IF'] = model.fit_predict(features)

    # Label anomalies (-1)
    df['Is_Anomaly_IF'] = df['Is_Anomaly_IF'] == -1
    anomalies = df[df['Is_Anomaly_IF'] == True]
    anomalies.to_csv(output_path, index=False)

    # Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Date', y='Revenue', label='Revenue')
    plt.scatter(anomalies['Date'], anomalies['Revenue'], color='orange', label='IsolationForest Anomalies')
    plt.title("Isolation Forest Revenue Anomalies")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/iforest_anomaly_plot.png")
    plt.close()
    print("✅ Isolation Forest anomalies saved and plotted.")