import pandas as pd
import numpy as np

def generate_business_data(save_path="data/bizpulse_data.csv"):
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='W')
    regions = ['North', 'South', 'East', 'West']
    units = ['Product A', 'Product B', 'Product C']
    data = []

    for date in dates:
        for region in regions:
            for unit in units:
                revenue = np.random.normal(loc=50000, scale=8000)
                marketing = np.random.normal(loc=10000, scale=2000)
                profit = revenue - marketing - np.random.normal(loc=5000, scale=1000)
                satisfaction = np.clip(np.random.normal(loc=4, scale=0.5), 1, 5)
                data.append([date, region, unit, revenue, profit, marketing, satisfaction])

    df = pd.DataFrame(data, columns=[
        'Date', 'Region', 'Business_Unit', 'Revenue', 'Profit',
        'Marketing_Spend', 'Customer_Satisfaction'
    ])

    df.to_csv(save_path, index=False)
    print(f"Data saved to {save_path}")