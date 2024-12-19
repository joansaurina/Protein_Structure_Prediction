import pandas as pd

def process_metrics(file_path):
    # Load data
    df = pd.read_csv(file_path)

    # Define columns of interest
    columns = [
        'pLDDT_Fold', 'PAE_Fold', 'pTM_Fold', 'RMSD_Fold',
        'pLDDT_Protenix', 'PAE_Protenix', 'pTM_Protenix',
        'RMSD_Protenix', 'PAE_Chai', 'pTM_Chai', 'RMSD_Chai'
    ]

    # Ensure numeric values are correctly formatted
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Define metric groups
    metrics_groups = {
        'PAE': [col for col in columns if 'PAE' in col],
        'pLDDT': [col for col in columns if 'pLDDT' in col],
        'pTM': [col for col in columns if 'pTM' in col],
        'RMSD': [col for col in columns if 'RMSD' in col]
    }

    # Calculate mean metrics by group
    mean_metrics = {
        'Metric Group': [],
        'Model': [],
        'Mean Value': []
    }

    for metric_name, metric_columns in metrics_groups.items():
        for col in metric_columns:
            model_name = col.split('_')[-1]  # Extract model name
            mean_value = df[col].mean()
            mean_metrics['Metric Group'].append(metric_name)
            mean_metrics['Model'].append(model_name)
            mean_metrics['Mean Value'].append(mean_value)

    # Create DataFrame for means
    df_mean_metrics = pd.DataFrame(mean_metrics)

    # Create pivot table for better visualization
    df_mean_pivot = df_mean_metrics.pivot(index='Metric Group', columns='Model', values='Mean Value')
    df_mean_pivot.index.name = None
    df_mean_pivot.columns.name = None

    # Display the table
    print('\n')
    print("Mean by metric group:")
    print('\n')
    print(df_mean_pivot)

    # Calculate mean metrics by difficulty level
    if 'Difficulty' in df.columns:
        mean_metrics_by_difficulty = {
            'Difficulty': [],
            'Metric Group': [],
            'Model': [],
            'Mean Value': []
        }

        for difficulty, group in df.groupby('Difficulty'):
            for metric_name, metric_columns in metrics_groups.items():
                for col in metric_columns:
                    model_name = col.split('_')[-1]
                    mean_value = group[col].mean()
                    mean_metrics_by_difficulty['Difficulty'].append(difficulty)
                    mean_metrics_by_difficulty['Metric Group'].append(metric_name)
                    mean_metrics_by_difficulty['Model'].append(model_name)
                    mean_metrics_by_difficulty['Mean Value'].append(mean_value)

        # Create DataFrame for means by difficulty
        df_mean_metrics_by_difficulty = pd.DataFrame(mean_metrics_by_difficulty)

        # Create pivot table for better visualization
        df_mean_pivot_by_difficulty = df_mean_metrics_by_difficulty.pivot(
            index=['Difficulty', 'Metric Group'],
            columns='Model',
            values='Mean Value'
        )
        df_mean_pivot_by_difficulty.index.names = [None, None]
        df_mean_pivot_by_difficulty.columns.name = None

        # Display the table
        print('\n')
        print("Mean by metric group and difficulty:")
        print('\n')
        print(df_mean_pivot_by_difficulty)
        print('\n')

if __name__ == "__main__":
    # Path to the CSV file
    file_path = 'data/data.csv'
    process_metrics(file_path)
