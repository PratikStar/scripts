# Status: Complete and working
# Description: Selects Winner randomly
# How to: python3 raffle-winner.py exports/20210905160610-timbre_survey.csv
import sys
import pandas as pd


if __name__ == '__main__':

    filename = sys.argv[1] # "20210905160610-timbre_survey.csv"

    print("\n\nLoading survey results...")
    df = pd.read_csv(filename)
    print("Randomly Selecting the winner...")

    print("The winner is: " + df.sample()['email'].to_string().split(' ')[-1])