## Project 1 (Data Visualization Portion) - Julian Crowley
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from data_scrub_project_JC import load_data, clean_nans, push_diet_data_to_csv

def load_avg_statistics(df,target_col,range_cols=[],ranges=[]):
    """ - Params: Target dateframe df, the target column (string) to get an average on, a list of columns (strings) for cross sectionality data,
                  and a list of lists (sub lists are lists of numbers corresponding to ranges) to specify cross sectionality.
        - Usage: Grabs the cross section of data within the ranges of each specified column,
                 and gets average of a target column for the range of data as list for each specified column.
        - Return: Returns a list of lists for average statistics, or None if range_cols and ranges are no same length
    """
    output=[]
    if len(range_cols)!=len(ranges): return None
    for i in range(len(range_cols)):
        sub_list=[]
        for range_pos in ranges[i]:
            sub_list.append(np.average(df.loc[df[range_cols[i]]==range_pos][target_col]))
        output.append(sub_list)
    return output

def plot_bar(x_data,height_data,ylabel,title,xlabel=None,c=None):
    """ - Params: The x data (list), height data (list of number), y label (string) for bar plot, 
                  the color of chart (string and optional), x label (string) for bar chart (optional),
                  and the title of the plot (string)
        - Usage: Constructs and displays the bar plot based on data provided
    """
    if c==None:plt.bar(x=x_data,height=height_data)
    else:plt.bar(x=x_data,height=height_data,color=c)
    plt.ylabel(ylabel)
    plt.title(title)
    if xlabel!=None: plt.xlabel(xlabel)
    plt.show()

def main():
    ##Load Data
    ##Uncomment Next Line to Running CSV Producer Function
    #push_diet_data_to_csv()
    patient_data=load_data("USA_NHANES_2013-2014_ParticipantData.csv",selected_cols=["id", "bmi_cat","clin_diet","edc_level_adults","hh_income"])
    diet_statistics=load_data("Diet Stats(No NAN).csv",selected_cols=["id","avg_energy","avg_carb"])
    combined_data=clean_nans(patient_data.merge(diet_statistics, on="id"))
    ##Define Range Constants and grab average participant meal/carb data
    avg_carbs_for_edc, avg_carbs_for_bmi, avg_carbs_for_income=load_avg_statistics(combined_data,"avg_carb",range_cols=["edc_level_adults","bmi_cat","hh_income"],ranges=[list(range(1,6)),list(range(1,5)),list(range(1,13))])
    ##Visualizations
    education_list=["9th Grade or Below","9th-12th Grade","High School Diploma","Attending College","College Graduate or Above"]
    plot_bar(education_list,avg_carbs_for_edc,"Carbs (G) Per Meal Per Participant","Education vs. Carbs per Meal")
    bmi_list=["Underweight BMI","Normal BMI", "Overweight BMI","Obese BMI"]
    plot_bar(bmi_list,avg_carbs_for_bmi,"Carbs (G) Per Meal Per Participant","BMI Types vs. Carbs Per Meal",c="green")
    income_list=["<5,000","<10,000","<15,000","<20,000","<25,000","<35,000","<45,000","<55,000","<65,000","<75,000","<100,00","100,000+"]
    plot_bar(income_list,avg_carbs_for_income,"Carbs (G) Per Meal Per Participant","Annual Household Income vs. Carbs Per Meal", xlabel="Annual Income ($)",c="purple")
    
    

main()