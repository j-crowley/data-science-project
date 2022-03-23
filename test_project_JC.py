## Project 1 (Unit Test Portion) - Julian Crowley
import unittest
import pandas as pd
import numpy as np
from data_scrub_project_JC import load_data, grab_avg_stats, clean_nans
from visualization_project_JC import load_avg_statistics

class TestProject(unittest.TestCase):
    def test_load_data(self):
        print("\nTesting load_data()")
        #Test Case 1: No Selected Columns
        test=load_data("test.csv")
        print("Test 1:")
        print(test)
        expected=pd.DataFrame([[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,3,4,4]],columns=["id","var1","var2","var3"])
        print("Expected:")
        print(expected)
        print()

        #Test Case 2: 1 Selected Columns
        test=load_data("test.csv",selected_cols=["id"])
        print("Test 2:")
        print(test)
        expected=pd.DataFrame([[1],[2],[3],[4]],columns=["id"])
        print("Expected:")
        print(expected)
        print()
        
        #Test Case 2: 3 Selected Columns
        test=load_data("test.csv",selected_cols=["id","var1","var3"])
        print("Test 3:")
        print(test)
        expected=pd.DataFrame([[1,1,1],[2,2,2],[3,3,3],[4,3,4]],columns=["id","var1","var3"])
        print("Expected:")
        print(expected)
        print()

    def test_grab_avg_stats(self):
        print("\nTesting grab_avg_stats()")
        #Test Case 1: No Modes
        test=grab_avg_stats(pd.DataFrame([[1,1,2,1],[1,2,2,2],[2,3,3,3],[2,3,6,6],[2,6,6,6]],columns=["id","red","blue","purple"])) 
        print("Test 1:")
        print(test)
        expected=pd.DataFrame([[1,1.5,2,1.5],[2,4,5,5]],columns=["id","avg_red","avg_blue","avg_purple"])
        print("Expected:")
        print(expected)
        print()

        #Test Case 1: 1 Modes
        test=grab_avg_stats(pd.DataFrame([[1,1,2,1],[1,2,2,2],[2,3,3,3],[2,3,6,6],[2,6,6,6]],columns=["id","red","blue","purple"]),col_not_avg=["blue"]) 
        print("Test 2:")
        print(test)
        expected=pd.DataFrame([[1,1.5,2,1.5],[2,4,6,5]],columns=["id","avg_red","avg_blue","avg_purple"])
        print("Expected:")
        print(expected)
        print()

    def test_clean_nans(self):
        print("\nTesting clean_nans()")
        #Test Case 1: No nans
        test=clean_nans(pd.DataFrame([[1,1,2,1],[1,2,2,2],[2,3,3,3]]))
        print("Test 1:")
        print(test)
        expected=pd.DataFrame([[1,1,2,1],[1,2,2,2],[2,3,3,3]])
        print("Expected:")
        print(expected)
        print()

        #Test Case 2: Some nans
        test=clean_nans(pd.DataFrame([[1,1,np.nan,1],[1,2,2,2],[2,3,np.nan,3]]))
        print("Test 2:")
        print(test)
        expected=pd.DataFrame([[1,2,2.0,2]],index=["1"])
        print("Expected:")
        print(expected)
        print()
    
    def test_load_avg_statistics(self):
        #Test Case 1: Ranges and Number of Columns Unequal
        test=pd.DataFrame()
        expected=None
        self.assertEqual(load_avg_statistics(test,target_col=None,range_cols=[],ranges=list(range(0,10))),expected)

        #Test Case 2: One Column and One Range
        test=pd.DataFrame([[1,1,1],[2,2,2],[2,3,2]],columns=["id","var1","var2"])
        expected=[[1.0,2.5]]
        self.assertEqual(load_avg_statistics(test,target_col="var1",range_cols=["var2"],ranges=[list(range(1,3))]),expected)

        #Test Case 3: Two Columns and Two Ranges
        test=pd.DataFrame([[1,1,1,1],[2,3,2,2],[2,3,2,2],[2,3,2,2]],columns=["id","var1","var2","var3"])
        print(test)
        expected=[[1.0,3.0],[1.0,3.0]]
        self.assertEqual(load_avg_statistics(test,target_col="var1",range_cols=["var2","var3"],ranges=[list(range(1,3)),list(range(1,3))]),expected)


def main():
    unittest.main(verbosity = 3)

main()