## Project 1 (Data Scrubbing Portion) - Julian Crowley
## DO NOT RUN LAST FUNCTION, scrubbing takes up to 30 minutes depending on system processing
import pandas as pd
from scipy import stats
import numpy as np

def load_data(filename,selected_cols=[]):
    """ - Params: Filename (string) of csv to import into pandas, and selected columns (list of strings) to return in the pandas dataframe.
        - Usage: Imports the selected csv from the file name and drops all other columns besides the ones in selected_cols if selected_cols is not empty.
                Otherwise keeps the pandas dataframe without any data manipulation.
        - Return: Returns a pandas dataframe.
    """
    output=pd.read_csv(filename)
    if len(selected_cols)==0:
        return output
    else:
        labels=output.columns
        del_labels=[]
        for label in labels:
            if label not in selected_cols: del_labels.append(label)
        output=output.drop(labels=del_labels,axis=1)
        return output

def grab_avg_stats(df,col_not_avg=[]):
    """ - Params: pandas dataframe of data (must have an id column), and a list of strings of which columns not to grab average statistics.
        - Usage: Creates a new pandas dataframe where all column statistics besides id are average, and columns specified by col_not_avg are 
                 turned into columns where the the most common of said column is grabbed as a statistic.
        - Returns: New dataframe with most common and average statistics.
    """
    ##Updated Column Headers
    cols=df.columns
    col_list=[]
    col_list.append("id")
    for i in range(1,len(cols)):
        if cols[i] in col_not_avg:
            col_list.append("mode_"+cols[i])
        else:
            col_list.append("avg_"+cols[i])
    id_list=[]
    ##Updated Data
    rows_list=[]
    for id_ref in df["id"]:
        if id_ref not in id_list:
            temp_dict={}
            for col in col_list:
                if col=="id": temp_dict["id"]=id_ref
                elif col.find("mode")!=-1: temp_dict[col]=stats.mode(df.loc[df["id"]==id_ref][col.lstrip("mode_")])[0][0]
                elif col.find("avg")!=-1: temp_dict[col]=np.nanmean(df.loc[df["id"]==id_ref][col.lstrip("avg_")])
            rows_list.append(temp_dict)
        id_list.append(id_ref)
    return pd.DataFrame(rows_list)

def clean_nans(df):
    """ - Params: pandas dataframe of data (must have an id column)
        - Usage: Creates a new pandas dataframe where all column save the id column have NAN's removed
        - Returns: New cleaned dataframe
    """
    new_df=df.dropna()
    return new_df

def push_diet_data_to_csv():
    """ - Usage: Creates a new dataframe of the combined datasets for diet data, cleans the data, aggregates statistics from the data,
                 and pushes that the new dataframe into a csv
    """
    ##Load Data
    diet_data_p1=load_data("USA_NHANES_2013-2014_DietData_part1.csv", selected_cols=["id","food_type","energy","carb"])
    diet_data_p2=load_data("USA_NHANES_2013-2014_DietData_part2.csv", selected_cols=["id","food_type","energy","carb"])
    ##Merge and Reconfigure Data
    diet_data_tot=pd.concat([diet_data_p1,diet_data_p2], ignore_index=True)
    diet_data_tot=clean_nans(diet_data_tot)
    diet_stats=grab_avg_stats(diet_data_tot,col_not_avg=["food_type"])
    print(diet_stats)
    ##Push Data to CSV
    diet_stats.to_csv('Diet Stats(No NAN).csv',index=False)
