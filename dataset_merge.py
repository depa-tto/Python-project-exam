"""
dataset_merge.py

This module is responsible for merging multiple datasets into a single cohesive dataset.
It includes functions for reading, cleaning, and combining data from various sources
and formats, ensuring consistency and removing duplicates.

Output Datasets:
1. 'merge_set':
   - Includes the variable 'region', which indicates all the states where each movie was released.
   - This dataset contain duplicates due to the inclusion of regional information.
   - Intended for creating a map with GeoPandas using the regional data.

2. 'game_set':
   - Excludes the 'region' variable, thereby eliminating duplicates associated with it.
   - Designed for basic descriptive analysis and for running the quiz game.

Data Source:
For more information about the variables and data structure, visit the Kaggle page:
https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset?select=title.basics.tsv
"""


import os  # type: ignore
import pandas as pd  # type: ignore
import opendatasets as od  # type: ignore
import numpy as np  # type: ignore

dataset = "https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset/data"

od.download(dataset)
data_dir = "./imdb-dataset"
os.listdir(data_dir)

roles_df = pd.read_table(
    "./imdb-dataset/name.basics.tsv", sep="\t"
)  # dataset regarding people
roles_df.drop(
    ["deathYear"], axis=1, inplace=True
)  # drop 'deathYear' becuase not all the instances have a death date
roles_df.replace("\\N", np.nan, inplace=True)
roles_df.dropna(inplace=True)  # drop all the missing values
roles_df[["first_profession", "second_profession", "third_profession"]] = roles_df[
    "primaryProfession"
].str.split(
    ",", expand=True
)  # divide 'primaryProfession' in 3 sub-columns
roles_df.drop(["primaryProfession"], axis=1, inplace=True)  # drop 'primaryProfession'
roles_df[["movie_1", "movie_2", "movie_3", "movie_4"]] = roles_df[
    "knownForTitles"
].str.split(
    ",", expand=True
)  # divide 'knownForTitles' in 4 sub-columns
roles_df.drop(["knownForTitles"], axis=1, inplace=True)  # drop 'knownForTitles'
roles_df = roles_df.rename(
    columns={
        "nconst": "name_id",
        "primaryName": "name_surname",
        "birthYear": "birth",
    }
)  # rename some initial columns


movie_df = pd.read_table(
    "./imdb-dataset/title.basics.tsv", sep="\t"
)  # dataset regarding movies
movie_df.drop(
    ["endYear", "originalTitle"], axis=1, inplace=True
)  # drop 'endYear' because 99% of the observations are missing values
# drop 'originalTitle' because it is not usefull
# the variable 'primaryTitle' is keept instead since is the more popular title
movie_df = movie_df.loc[
    (movie_df["titleType"] == "tvSeries") | (movie_df["titleType"] == "movie")
]  # keep only tv series and movies in the dataset
movie_df.replace("\\N", np.nan, inplace=True)
movie_df.dropna(inplace=True)  # drop all the missing values
movie_df[["genre_1", "genre_2", "genre_3"]] = movie_df["genres"].str.split(
    ",", expand=True
)  # split the 'genres' variable in 3 sub-columns
movie_df.drop(["genres"], axis=1, inplace=True)
movie_df = movie_df.rename(
    columns={
        "tconst": "movie_id",
        "titleType": "type",
        "primaryTitle": "title",
        "isAdult": "adult",
        "startYear": "start_year",
        "runtimeMinutes": "minutes_runtimes",
    }
)  # rename some initial variables
movie_df["type"] = movie_df["type"].replace({"tvSeries": "tv series"})

region_df = pd.read_table(
    "./imdb-dataset/title.akas.tsv", sep="\t", usecols=["titleId", "region"]
)  # dataset about the states where tv series and movies are released
region_df.replace("\\N", np.nan, inplace=True)
region_df.dropna(inplace=True)  # drop all the missing values

merge_set1 = pd.merge(roles_df, movie_df, left_on="movie_1", right_on="movie_id").drop(
    ["movie_1", "movie_2", "movie_3", "movie_4", "name_id"], axis=1
)  # inner join between roles_df and movie_df on movie_1
merge_set2 = pd.merge(roles_df, movie_df, left_on="movie_2", right_on="movie_id").drop(
    ["movie_1", "movie_2", "movie_3", "movie_4", "name_id"], axis=1
)  # inner join between roles_df and movie_df on movie_2
merge_set3 = pd.merge(roles_df, movie_df, left_on="movie_3", right_on="movie_id").drop(
    ["movie_1", "movie_2", "movie_3", "movie_4", "name_id"], axis=1
)  # inner join between roles_df and movie_df on movie_3
merge_set4 = pd.merge(roles_df, movie_df, left_on="movie_4", right_on="movie_id").drop(
    ["movie_1", "movie_2", "movie_3", "movie_4", "name_id"], axis=1
)  # inner join between roles_df and movie_df on movie_4
merge_set = pd.concat(
    [merge_set1, merge_set2, merge_set3, merge_set4]
)  # concatention of the 4 merged datasets
# final dataset called 'merge_set' is obtained
merge_set.drop_duplicates(inplace=True)  # drop duplicates
pd.merge(merge_set, region_df, left_on="movie_id", right_on="titleId").drop(
    ["movie_id", "titleId"], axis=1, inplace=True
)  # inner join between merge_set and region_df

merge_set["first_profession"] = merge_set["first_profession"].str.replace("_", " ")
merge_set["start_year"] = (
    pd.to_numeric(merge_set["start_year"], errors="coerce").fillna(0).astype(int)
)  # convert 'start_year' variable into numeric type

merge_set.drop_duplicates(inplace=True)
merge_set.to_csv("merge_set.csv", index=False)  # save the merge_set as a csv file
# merge_set dataset will be used for geopandas map

game_set = pd.read_csv("./merge_set.csv")
game_set.drop(
    ["region"], axis=1, inplace=True
)  # drop the region variable from the game set since will not be used for the quiz game
game_set.drop_duplicates(
    inplace=True
)  # remove all the duplicates that the variable 'region' has
game_set.to_csv("game_set.csv", index=False)  # save the game_set as a csv file
