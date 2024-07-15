import pandas as pd
import numpy as np
from io import StringIO

def my_m_and_a(file1, file2, file3):
    # Load datasets
    df_main = pd.read_csv(file1)
    df_aux1 = pd.read_csv(file2, sep=";", header=None, names=["Age", "City", "Gender", "Name", "Email"])
    df_aux2 = pd.read_csv(file3, sep="\t", skiprows=1, names=["Gender", "Name", "Email", "Age", "City", "Country"])

    # Replace spaces in column names with underscores
    df_main.columns = df_main.columns.str.replace(' ', '_')
    df_aux1.columns = df_aux1.columns.str.replace(' ', '_')
    df_aux2.columns = df_aux2.columns.str.replace(' ', '_')

    # Standardize Gender
    gender_mapping = {"0": "Male", "1": "Female", "F": "Female", "M": "Male"}
    df_main['Gender'] = df_main['Gender'].replace(gender_mapping)
    df_aux1['Gender'] = df_aux1['Gender'].replace(gender_mapping).str.title()
    df_aux2['Gender'] = df_aux2['Gender'].str.replace("string_|character_|boolean_", "", regex=True).replace(gender_mapping)

    # Clean and format df_main
    df_main['FirstName'] = df_main['FirstName'].astype(str).str.replace(r"\W", "", regex=True).str.title()
    df_main['LastName'] = df_main['LastName'].astype(str).str.replace(r"\W", "", regex=True).str.title()
    df_main['Email'] = df_main['Email'].astype(str).str.lower()
    df_main['City'] = df_main['City'].astype(str).str.replace("_", "-", regex=False).str.title()
    df_main['Country'] = "USA"
    df_main = df_main.drop(columns=['UserName'])

    # Clean and format df_aux1
    df_aux1['Age'] = df_aux1['Age'].astype(str).str.replace(r"\D", "", regex=True)
    df_aux1['City'] = df_aux1['City'].astype(str).str.replace("_", "-", regex=False).str.title()
    names_split = df_aux1['Name'].astype(str).str.split(expand=True)
    df_aux1['FirstName'] = names_split[0].str.replace(r"\W", "", regex=True).str.title()
    df_aux1['LastName'] = names_split[1].str.replace(r"\W", "", regex=True).str.title()
    df_aux1['Email'] = df_aux1['Email'].astype(str).str.lower()
    df_aux1['Country'] = 'USA'
    df_aux1 = df_aux1.drop(columns=['Name'])

    # Clean and format df_aux2
    df_aux2['Email'] = df_aux2['Email'].astype(str).str.replace("string_", "", regex=False).str.lower()
    df_aux2['Age'] = df_aux2['Age'].astype(str).str.replace(r"\D", "", regex=True)
    df_aux2['City'] = df_aux2['City'].astype(str).str.replace("string_", "", regex=False).str.replace("_", "-", regex=False).str.title()
    names_split = df_aux2['Name'].astype(str).str.split(expand=True)
    df_aux2['FirstName'] = names_split[0].str.replace(r"\W", "", regex=True).str.title()
    df_aux2['LastName'] = names_split[1].str.replace(r"\W", "", regex=True).str.title()
    df_aux2['Country'] = 'USA'

    # Concatenate all dataframes
    combined_df = pd.concat([df_main, df_aux1, df_aux2], ignore_index=True)

    # Reorder and ensure column types
    final_columns = ["Gender", "FirstName", "LastName", "Email", "Age", "City", "Country"]
    combined_df = combined_df[final_columns]
    combined_df['FirstName'] = combined_df['FirstName'].astype(str)
    combined_df['LastName'] = combined_df['LastName'].astype(str)
    combined_df['Age'] = combined_df['Age'].astype(str)

    return combined_df
