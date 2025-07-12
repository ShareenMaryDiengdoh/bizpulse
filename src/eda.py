import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set default style
sns.set(style="whitegrid")

def run_eda(data_path="data/bizpulse_data.csv"):
    df = pd.read_csv(data_path, parse_dates=['Date'])

    print("✅ Data loaded successfully!")
    print(df.head())
    print("\n📊 Dataset Info:")
    print(df.info())
    print("\n📈 Summary Stats:")
    print(df.describe())

    # Revenue trend by Region
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df, x='Date', y='Revenue', hue='Region')
    plt.title("Revenue Trend by Region")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/revenue_trend_by_region.png")
    plt.close()

    # Profit distribution by Region
    plt.figure(figsize=(8,5))
    sns.boxplot(data=df, x='Region', y='Profit')
    plt.title("Profit Distribution by Region")
    plt.tight_layout()
    plt.savefig("output/profit_distribution_by_region.png")
    plt.close()

    # Correlation heatmap
    plt.figure(figsize=(6,5))
    numeric_cols = ['Revenue', 'Profit', 'Marketing_Spend', 'Customer_Satisfaction']
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Between Business Metrics")
    plt.tight_layout()
    plt.savefig("output/correlation_matrix.png")
    plt.close()

    print("📁 Plots saved to /output folder.")

    # Optional: Interactive Plotly chart
    fig = px.line(df, x='Date', y='Revenue', color='Region', title='Interactive Revenue Trend by Region')
    fig.write_html("output/interactive_revenue_plot.html")
    print("🌐 Interactive plot saved to output/interactive_revenue_plot.html")