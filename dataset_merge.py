import pandas as pd # type: ignore
import os # type: ignore
import opendatasets as od # type: ignore
import numpy as np # type: ignore

dataset = 'https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset/data'

od.download(dataset)
data_dir = './imdb-dataset'
os.listdir(data_dir)

roles_df = pd.read_table('./imdb-dataset/name.basics.tsv', sep='\t')
roles_df.replace('\\N', np.nan, inplace=True)
roles_df.dropna(inplace=True)
roles_df[['first_profession', 'second_profession', 'third_profession']] = roles_df['primaryProfession'].str.split(',', expand=True)
roles_df = roles_df.drop(['primaryProfession'], axis = 1)
roles_df[['movie_1', 'movie_2', 'movie_3', 'movie_4']] = roles_df['knownForTitles'].str.split(',', expand=True)
roles_df = roles_df.drop(['knownForTitles'], axis = 1)
roles_df = roles_df.rename(columns={'nconst': 'name_id',
                                    'primaryName': 'name_surname',
                                    'birthYear': 'birth',
                                    'deathYear': 'death'})


movie_df = pd.read_table('./imdb-dataset/title.basics.tsv', sep='\t')
movie_df.replace('\\N', np.nan, inplace=True)
movie_df.dropna(inplace=True)
movie_df[['genre_1', 'genre_2', 'genre_3']] = movie_df['genres'].str.split(',', expand=True)
movie_df  = movie_df.drop(['genres'], axis = 1)
movie_df = movie_df.rename(columns = {'tconst': 'movie_id',
                                      'titleType': 'type',
                                      'primaryTitle': 'title',
                                      'originalTitle': 'original_title',
                                      'isAdult': 'adult',
                                      'startYear': 'start_year',
                                      'endYear': 'end_year',
                                      'runtimeMinutes': 'minutes_runtimes'})



region_df = pd.read_table('./imdb-dataset/title.akas.tsv', sep='\t', usecols=['titleId', 'region'])
region_df.replace('\\N', np.nan, inplace=True)
region_df.dropna(inplace=True)


print(roles_df)
print(movie_df)
print(region_df)

merge_set1 = pd.merge(roles_df, movie_df, left_on='movie_1', right_on='movie_id').drop(
    ['movie_1', 'movie_2', 'movie_3', 'movie_4', 'name_id'], axis = 1)
merge_set2 = pd.merge(roles_df, movie_df, left_on='movie_2', right_on='movie_id').drop(
    ['movie_1', 'movie_2', 'movie_3', 'movie_4', 'name_id'], axis = 1)
merge_set3 = pd.merge(roles_df, movie_df, left_on='movie_3', right_on='movie_id').drop(
    ['movie_1', 'movie_2', 'movie_3', 'movie_4', 'name_id'], axis = 1)
merge_set4 = pd.merge(roles_df, movie_df, left_on='movie_4', right_on='movie_id').drop(
    ['movie_1', 'movie_2', 'movie_3', 'movie_4', 'name_id'], axis = 1)
merge_set = pd.concat([merge_set1, merge_set2, merge_set3, merge_set4])
merge_set = pd.merge(merge_set, region_df, left_on='movie_id', right_on='titleId').drop(['movie_id', 'titleId'], axis = 1)
merge_set['type'] = merge_set['type'].replace({'tvSeries': 'tv series', 'tvMiniSeries': 'tv mini Series'})
merge_set['first_profession'] = merge_set['first_profession'].str.replace('_', ' ')
merge_set['first_profession'].unique()
merge_set['start_year'] = pd.to_numeric(merge_set['start_year'], errors='coerce').fillna(0).astype(int)

print(merge_set)
merge_set.to_csv('merge_set.csv')