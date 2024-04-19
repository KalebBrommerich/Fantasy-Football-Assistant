import pandas as pd

def remove_repeated_headers(df):
    header = df.columns
    for col in header:
        df = df[df[col] != col]
    return df

def calculate_fantasy_points(df, file_path):
    # Convert the 'Yds' and 'TD' columns to numeric type, ignoring errors
    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')

    # Calculate fantasy points based on the file name
    if 'passing' in file_path:
        df['Fantasy_Points'] = df['Yds'] / 25 + df['TD'] * 4
    elif 'rushing' in file_path:
        df['Fantasy_Points'] = df['Yds'] / 10 + df['TD'] * 6
    elif 'receiving' in file_path:
        df['Fantasy_Points'] = df['Yds'] / 10 + df['TD'] * 6
    return df

def convert_percent_to_float(df):
    """
    Convert percentage string columns to float. Assumes percentages are represented as '85.0%'
    and converts them to float format 0.85.
    """
    percent_columns = [col for col in df.columns if '%' in col]
    for col in percent_columns:
        df[col] = df[col].str.rstrip('%').astype('float') / 100.0
    return df

def round_dataframe(df):
    """
    Rounds all numeric columns in the dataframe to three decimal places.
    """
    numeric_cols = df.select_dtypes(include=['float64', 'float32'])
    df[numeric_cols.columns] = numeric_cols.round(3)
    return df



def process_and_merge(files_and_years,years):
    passing_data = []
    rushing_data = []
    receiving_data = []

    for file_path, year in files_and_years:
        df = pd.read_csv(file_path)
        df = remove_repeated_headers(df)
        df = convert_percent_to_float(df)
        df['Year'] = year
        if 'passing' in file_path:
            df = df[df['Pos'] == 'QB']
            df.drop(['4QC', 'GWD', 'QBrec'], axis=1, inplace=True)
        if 'rushing' in file_path:
            df = df[df['Pos'] == 'RB']
        df.drop(['Pos', 'Tm', 'Rk'], axis=1, inplace=True)
        df = df.dropna()
        df = calculate_fantasy_points(df, file_path)
        df = df.loc[df['Fantasy_Points'] >= 100]
        df = round_dataframe(df)

        if "passing" in file_path:
            passing_data.append(df)
        elif "rushing" in file_path:
            rushing_data.append(df)
        elif "receiving" in file_path:
            receiving_data.append(df)

    # Process dataframes for each category
    for dataset, name in [(passing_data, 'passing'), (rushing_data, 'rushing'), (receiving_data, 'receiving')]:
        combined_df = pd.concat(dataset)
        
        # Ensure to sort by player and year in descending order
        combined_df.sort_values(by=['Player', 'Year'], ascending=[True, False], inplace=True)

        # Apply a filter to ensure only players with at least 3 entries are considered
        filtered_df = combined_df.groupby('Player').filter(lambda x: len(x) >= 3)

        # After filtering, take the top 3 entries
        filtered_df = filtered_df.groupby('Player').head(3)
        
        # Sort by player and year in ascending order for the final output
        filtered_df.sort_values(by=['Player', 'Year'], ascending=[True, True], inplace=True)
        
        filtered_df.to_csv(f'combined_{name}_{years}.csv', index=False)




# List of file paths and corresponding years
files_and_years = [
    (r'TrainingData/2018/passing.csv', 2018),
    (r'TrainingData/2018/rushing.csv', 2018),
    (r'TrainingData/2018/receiving.csv', 2018),
    (r'TrainingData/2019/passing.csv', 2019),
    (r'TrainingData/2019/rushing.csv', 2019),
    (r'TrainingData/2019/receiving.csv', 2019),
    (r'TrainingData/2020/passing.csv', 2020),
    (r'TrainingData/2020/rushing.csv', 2020),
    (r'TrainingData/2020/receiving.csv', 2020),
    (r'TrainingData/2021/passing.csv', 2021),
    (r'TrainingData/2021/rushing.csv', 2021),
    (r'TrainingData/2021/receiving.csv', 2021),
    (r'TrainingData/2022/passing.csv', 2022),
    (r'TrainingData/2022/rushing.csv', 2022),
    (r'TrainingData/2022/receiving.csv', 2022),
    (r'TrainingData/2023/passing.csv', 2023),
    (r'TrainingData/2023/rushing.csv', 2023),
    (r'TrainingData/2023/receiving.csv', 2023)
]
# List of file paths and corresponding years
files_and_years2 = [
    (r'TrainingData/2012/passing.csv', 2012),
    (r'TrainingData/2012/rushing.csv', 2012),
    (r'TrainingData/2012/receiving.csv', 2012),
    (r'TrainingData/2013/passing.csv', 2013),
    (r'TrainingData/2013/rushing.csv', 2013),
    (r'TrainingData/2013/receiving.csv', 2013),
    (r'TrainingData/2014/passing.csv', 2014),
    (r'TrainingData/2014/rushing.csv', 2014),
    (r'TrainingData/2014/receiving.csv', 2014),
    (r'TrainingData/2015/passing.csv', 2015),
    (r'TrainingData/2015/rushing.csv', 2015),
    (r'TrainingData/2015/receiving.csv', 2015),
    (r'TrainingData/2016/passing.csv', 2016),
    (r'TrainingData/2016/rushing.csv', 2016),
    (r'TrainingData/2016/receiving.csv', 2016),
    (r'TrainingData/2017/passing.csv', 2017),
    (r'TrainingData/2017/rushing.csv', 2017),
    (r'TrainingData/2017/receiving.csv', 2017)
]

# Process and merge the files
process_and_merge(files_and_years,'2018_2023')
process_and_merge(files_and_years2,'2012_2017')

