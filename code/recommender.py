import pandas as pd
import numpy as np
import lenskit, binpickle, datetime
from lenskit.datasets import MovieLens
import pathlib

class Recommender:
    def __init__(self, algorithms_path, data_movies, data_users, data_links):
        self._algorithms_path = algorithms_path
        self._algorithms_list = list(pathlib.Path(self._algorithms_path).iterdir())
        self._algorithm = binpickle.load(str(self._algorithms_list[0]))
        self._data_movies = data_movies
        self._data_users = data_users
        self._data_links = data_links

    def recommend(self, movies:pd.DataFrame, n_recs:int = 10, pop_bias:float = 1, year_bias:float = 1):
        recs = self._algorithm.recommend(-1, n_recs*10,ratings=movies)
        recs = recs.join(self._data_movies.title, on="item").join(self._data_links.drop(columns=["imdbId"]), on="item")
        year = datetime.datetime.today().year
        recs = recs.dropna()
        recs.score =    recs.score + \
                        np.log(recs.votes)*pop_bias/50 + \
                        np.sqrt(year - recs.year.astype(int))*year_bias/10
        answer = recs.sort_values(by="score", ascending=False).reset_index(drop=True).head(n_recs)
        answer.index += 1
        return answer[["item", "title", "score", "year", "runtime_min", "votes"]]
    
    def set_algorithm(self, new_algorithm):
        self._algorithm = binpickle.load(str(self._algorithms_path/new_algorithm))
    