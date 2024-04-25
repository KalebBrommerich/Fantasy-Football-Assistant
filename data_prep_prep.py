import pandas as pd

"""
data_prep_prep file
This file is used to clean the data before it is used in the prediction model classes,
it requires more data work to be able to predict, but this is a good clean start that can be understood by the user. 

functions here include

remove repeated headers
calculate fantasy points
convert percent to float
round dataframe

the above are all self-explanatory

process and merge is a long function which uses the above as helpers to process the data and merge it into larger datasets, these are used by data_preperation to create the sequences


"""

def remove_repeated_headers(df):
    """
    Remove rows that contain the same values as the column headers.
    They repeat around every 30 rows in the untouched data
    """
    header = df.columns
    for col in header:
        df = df[df[col] != col]
    return df

def calculate_fantasy_points(df, file_path):
    """
    Calculate fantasy points based on the file name. Needs to take ScoringConfig.txt as input. 
    """
    # Convert the 'Yds' and 'TD' columns to numeric type, ignoring errors
    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')

    # Calculate fantasy points based on the file name
    if 'passing' in file_path:
        df['Fantasy_Points'] = df['Yds'] / 25 + df['TD'] * 4
    elif 'rushing' in file_path:
        df['Fantasy_Points'] = df['Yds'] / 10 + df['TD'] * 6 
    elif 'receiving' in file_path:
        df['Rec'] = pd.to_numeric(df['Rec'], errors='coerce')
        df['Fantasy_Points'] = df['Yds'] / 10 + df['TD'] * 6 + df['Rec'] * 0.5
    return df

def convert_percent_to_float(df):
    """
    Convert percentage string columns to float. Assumes percentages are represented as '85.0'
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
        df = pd.read_csv(file_path) #Read CSV
        df = remove_repeated_headers(df) #Remove Headers
        df = convert_percent_to_float(df) #Convert percentage columns to float
        df = calculate_fantasy_points(df, file_path) #Calculate Fantasy Points
        df['Year'] = year #Add year column

        if 'passing' in file_path: #If passing, then filter out bad passing columns and filter for QB
            df = df[df['Pos'] == 'QB']
            df.drop(['4QC', 'GWD', 'QBrec',], axis=1, inplace=True)
            df = df.loc[df['Fantasy_Points'] >= 100] #Filter out players with less than 100 attempts, these outliers break the MinMaxScaler
        if 'rushing' in file_path: #If rushing, then for filter for RB
            df = df[df['Pos'] == 'RB']
            df = df.loc[df['Fantasy_Points'] >= 50]
        if 'receiving' in file_path:
            df = df.loc[df['Fantasy_Points'] >= 50]

        df.drop(['Pos', 'Tm', 'Rk'], axis=1, inplace=True) #Drop string based columns (they dont help in prediction)
        df = df.dropna() #Drop rows with missing values
        #df = df.loc[df['Fantasy_Points'] >= 100] #Filter out players with less than 100 fantasy points, these outliers break the MinMaxScaler
        df = round_dataframe(df) #Round all numeric columns to 3 decimal places, maybe not important, but it looks nice

        df['Player'] = df['Player'].str.replace(r'[\*\+]', '', regex=True)  # Remove special characters from player names

        if "passing" in file_path: #this is for the merge function, appending the dfs to a list to be combined 
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

        # Apply a filter to ensure only players with at least 3 entries are considered, this is for the learning model, 
        filtered_df = combined_df.groupby('Player').filter(lambda x: len(x) >= 3)      #would require a lot more data science to work without this 

        # After filtering, take the top 3 entries
        filtered_df = filtered_df.groupby('Player').head(3) #I am kind of unsure about what this line does... but I am scared to delete it
        
        # Sort by player and year in ascending order for the final output
        filtered_df.sort_values(by=['Player', 'Year'], ascending=[True, True], inplace=True)
        
        filtered_df.to_csv(f'TrainingData/combined_{name}_{years}.csv', index=False) # Save the final output to a CSV file in the TrainingData folder

# List of file paths and corresponding years
#Currently provided prediction data 
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

#Currently provided training data
# List of file paths and corresponding years
files_and_years2 = [
    (r'TrainingData/2006/rushing.csv', 2006),
    (r'TrainingData/2006/receiving.csv', 2006),
    (r'TrainingData/2006/passing.csv', 2006),
    (r'TrainingData/2007/rushing.csv', 2007),
    (r'TrainingData/2007/receiving.csv', 2007),
    (r'TrainingData/2007/passing.csv', 2007),
    (r'TrainingData/2008/rushing.csv', 2008),
    (r'TrainingData/2008/receiving.csv', 2008),
    (r'TrainingData/2008/passing.csv', 2008),
    (r'TrainingData/2009/rushing.csv', 2009),
    (r'TrainingData/2009/receiving.csv', 2009),
    (r'TrainingData/2009/passing.csv', 2009),
    (r'TrainingData/2010/rushing.csv', 2010),
    (r'TrainingData/2010/receiving.csv', 2010),
    (r'TrainingData/2010/passing.csv', 2010),
    (r'TrainingData/2011/receiving.csv', 2011),
    (r'TrainingData/2011/rushing.csv', 2011),
    (r'TrainingData/2011/passing.csv', 2011),
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
process_and_merge(files_and_years2,'2006_2017')

