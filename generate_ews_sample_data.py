import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

def generate_sample_data(num_rows=1000):
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(num_rows)]
    
    # Base values with some randomness
    base_volume = 1000
    base_inventory = 500
    base_loan = 2000
    base_balance = 2500
    
    # Generate data with realistic patterns
    data = {
        'date': dates,
        'actual_volume': [
            max(0, base_volume + np.random.normal(0, 200) + 100 * np.sin(x/30)) 
            for x in range(num_rows)
        ],
        'target_volume': [
            base_volume * 1.2 + np.random.normal(0, 100)
            for _ in range(num_rows)
        ],
        'actual_inventory': [
            max(0, base_inventory + np.random.normal(0, 100) + 50 * np.sin(x/45))
            for x in range(num_rows)
        ],
        'planned_inventory': [
            base_inventory + np.random.normal(0, 50)
            for _ in range(num_rows)
        ],
        'outstanding_loan_other': [
            max(0, base_loan * 0.1 + np.random.normal(0, 100))
            for _ in range(num_rows)
        ],
        'credit_limit': [base_loan for _ in range(num_rows)],
        'cash_balance': [
            max(0, base_balance + np.random.normal(0, 300) + 200 * np.sin(x/60))
            for x in range(num_rows)
        ],
        'loan_amount': [
            max(0, base_balance * 0.8 + np.random.normal(0, 200))
            for _ in range(num_rows)
        ],
        'account_balance': [
            max(0, base_balance + np.random.normal(0, 250) + 150 * np.sin(x/40))
            for x in range(num_rows)
        ]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Round all numeric columns to 2 decimal places
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].round(2)
    
    # Sort by date
    df = df.sort_values('date')
    
    return df

if __name__ == "__main__":
    # Generate sample data
    df = generate_sample_data(1000)
    
    # Save to CSV
    output_file = "ews_sample_data.csv"
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} rows of sample data in {output_file}")
    
    # Display some statistics
    print("\nData Statistics:")
    print(df.describe())
    
    # Display first few rows
    print("\nFirst few rows:")
    print(df.head())