import os
import ttkbootstrap as ttk
import pathlib
from ttkbootstrap.constants import *
from ttkbootstrap import utility
from tkinter import font
from recommender import *
from ttkwidgets.autocomplete import AutocompleteEntry
    

class RecommenderEngine(ttk.Frame, Recommender):
    def __init__(self, master, algorithms_path, data_movies, data_users, data_links):
        
        
        ttk.Frame.__init__(self, master, padding=15)
        Recommender.__init__(self, algorithms_path, data_movies, data_users, data_links)

        self.pack(fill=BOTH, expand=YES)

        self.defaultFont = font.nametofont("TkMenuFont")
        self.defaultFont.configure(family="open look cursor",
                                   size=18)

        # application variables
        self.chosen_algorithm = ttk.StringVar()
        self.user_id = ttk.DoubleVar(value=283229)
        self.n_recs = ttk.DoubleVar(value=10)

        self.pop_bias = ttk.DoubleVar(value=0)
        self.year_bias = ttk.DoubleVar(value=0)

        # header and labelframe option container
        option_text = "Complete the form to get your recommendations"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=10)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_entry_row()
        self.create_type_row()
        self.create_results_view()

    def create_entry_row(self):
        """Add term row to labelframe"""
        term_row = ttk.Frame(self.option_lf)
        term_row.pack(fill=X, expand=YES)
        
        label_user_id = ttk.Label(term_row, text="User id: ")
        label_user_id.pack(side=LEFT, padx=15)   
        user_id = ttk.Entry(term_row, textvariable=self.user_id, takefocus=True, width=8, justify=CENTER)
        user_id.pack(side=LEFT, fill=X, padx=1, pady=10)
        
        ttk.Label(term_row).pack(side=LEFT, padx=20)

        n_recs = ttk.Label(term_row, text="Number of recommendations: ")
        n_recs.pack(side=LEFT)   
        n_recs = ttk.Entry(term_row, textvariable=self.n_recs, width=5, justify=CENTER)
        n_recs.pack(side=LEFT, fill=X, padx=1)

        algorithm_combobox = ttk.Combobox(
            master=term_row,
            text="Choose the algorithm",
            values=list(map(lambda x: x.name, self._algorithms_list)),
            textvariable=self.chosen_algorithm,
            state="readonly",
            width=25
    )
        algorithm_combobox.current(0)
        algorithm_combobox.pack(side=LEFT, fill=X, padx=35)
        algorithm_combobox.bind('<<ComboboxSelected>>', self.on_select_algorithm)

        recommend_btn = ttk.Button(
            master=term_row, 
            text="Recommend me!", 
            command=self.on_recommend_me, 
            bootstyle=OUTLINE, 
            width=18
        )
        recommend_btn.pack(side=RIGHT, padx=20)

    def create_type_row(self):
        """Add type row to labelframe"""
        type_row = ttk.Frame(self.option_lf)
        type_row.pack(fill=X, expand=YES)
        type_lbl = ttk.Label(type_row, text="Biases", width=8)
        type_lbl.pack(side=LEFT, padx=(15, 0))
        
        ttk.Label(type_row, text='Less popular or more popular?:').pack(side=LEFT)
        slider_pop_bias = ttk.Scale(
            type_row,
            from_=-5,
            to=5,
            orient='horizontal',
            variable=self.pop_bias
        )
        
        slider_pop_bias.pack(side=LEFT, padx=20)
        ttk.Label(type_row, text='Newer or older?').pack(side=LEFT)
        slider_year_bias = ttk.Scale(
            type_row,
            from_=-5,
            to=5,
            orient='horizontal',
            variable=self.year_bias,
        )
        slider_year_bias.pack(side=LEFT, padx=10)
        slider_year_bias.pack()
        add_user_btn = ttk.Button(
            master=type_row, 
            text="Add user/movie", 
            command=self.open_user_window, 
            bootstyle=OUTLINE, 
            width=18
        )
        add_user_btn.pack(side=RIGHT, padx=20, pady=5)

    def create_results_view(self):
        """Add result treeview to labelframe"""
        self.resultview = ttk.Treeview(
            master=self, 
            bootstyle=INFO, 
            columns=[0, 1, 2, 3, 4, 5],
            show=HEADINGS,
            selectmode="browse"
        )
        self.resultview.pack(fill=BOTH, expand=YES, pady=10)
        verscrlbar = ttk.Scrollbar(self.resultview,
                           orient ="vertical",
                           command = self.resultview.yview)
        verscrlbar.pack(side ='right', fill ='y')
        self.resultview.configure(xscrollcommand = verscrlbar.set)
        # setup columns and use `scale_size` to adjust for resolution
        self.resultview.heading(0, text='Rank', anchor=W)
        self.resultview.heading(1, text='Title', anchor=W)
        self.resultview.heading(2, text='Year', anchor=W)
        self.resultview.heading(3, text='Score', anchor=W)
        self.resultview.heading(4, text='Runtime', anchor=W)
        self.resultview.heading(5, text='Votes', anchor=W)
        self.resultview.column(
            column=0, 
            anchor=W, 
            width=utility.scale_size(self, 50), 
            stretch=False
        )
        self.resultview.column(
            column=1, 
            anchor=W, 
            width=utility.scale_size(self, 300), 
            stretch=False
        )
        self.resultview.column(
            column=2, 
            anchor=W, 
            width=utility.scale_size(self, 130), 
        )
        self.resultview.column(
            column=3, 
            anchor=W, 
            width=utility.scale_size(self, 130), 

        )
        self.resultview.column(
            column=4, 
            anchor=W, 
            width=utility.scale_size(self, 120)
        )
        
        self.resultview.column(
            column=4, 
            anchor=W, 
            width=utility.scale_size(self, 160)
        )

    def on_recommend_me(self):
        user_id = int(self.user_id.get())
        n_recs = int(self.n_recs.get())
        pop_bias = self.pop_bias.get()
        year_bias = self.year_bias.get()
        
        children = self.resultview.get_children()

        if children != ():
            self.resultview.delete(*children)

        movies_ratings = self.get_user_ratings(user_id)

        recommendations = self.recommend(movies_ratings, n_recs, pop_bias, year_bias)
        for index_, row  in enumerate(recommendations.values): 
            rank = index_ + 1
            title = row[1]
            score = round(row[2], 2)
            release_year = row[3]
            runtime = row[4]
            votes = row[5]
            iid = self.resultview.insert(
                    parent='', 
                    index=END, 
                    values=(rank, title, release_year, score, runtime, votes)
                )
    
    def open_user_window(self):
            self.new_window = User(ttk.Toplevel("Add user/movies"), self._data_movies, self._data_users, self._data_links)
    
    def get_user_ratings(self, user_id):
        movies_ratings = self._data_users.query(f"user == {user_id}").set_index("item").rating
        return movies_ratings
    
    def on_select_algorithm(self, _):
        new_algorithm = self.chosen_algorithm.get()
        self.set_algorithm(new_algorithm)
        
class User(ttk.Frame):
    def __init__(self, master, data_movies, data_users, data_links):
        ttk.Frame.__init__(self, master, padding=15, width=900, height=600)
        self._data_links = data_links
        self._data_movies = data_movies
        self._data_users = data_users

        self._last_index = self._data_users.index[-1]
        self.pack(fill=BOTH, expand=YES)
        self.defaultFont = font.nametofont("TkMenuFont")
        self.defaultFont.configure(family="open look cursor",
                                   size=18)
        # application variables
        self.user_id = ttk.IntVar(value=1)
        self.movie_title = ttk.StringVar()
        self.rating = ttk.DoubleVar()
        # header and labelframe option container
        option_text = "Complete the form add a new movie or user"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_term_row()
        self.create_results_view()

    def create_term_row(self):
        """Add term row to labelframe"""
        term_row = ttk.Frame(self.option_lf)
        term_row.pack(fill=X, expand=YES)
        
        label_user_id = ttk.Label(term_row, text="User id: ")
        label_user_id.pack(side=LEFT, padx=15)   
        user_id = ttk.Entry(term_row, textvariable=self.user_id, takefocus=True, width=8, justify=CENTER)
        user_id.pack(side=LEFT, fill=X, padx=1, pady=10)
        
        ttk.Label(term_row).pack(side=LEFT, padx=20)

        movie_title = ttk.Label(term_row, text="Movie title: ")
        movie_title.pack(side=LEFT)   
        movie_title = AutocompleteEntry(term_row, textvariable=self.movie_title, justify=CENTER, completevalues=self._data_movies.title, width=25)
        movie_title.pack(side=LEFT, fill=X, padx=15)

        rating = ttk.Label(term_row, text="Rating: ")
        rating.pack(side=LEFT)   
        rating = ttk.Entry(term_row, textvariable=self.rating, width=5, justify=CENTER)
        rating.pack(side=LEFT, fill=X, padx=1)

        
        add_movie_btn = ttk.Button(
            master=term_row, 
            text="Add movie", 
            command=self.add_user_entry,
            bootstyle=OUTLINE, 
            width=18
        )
        add_movie_btn.pack(side=RIGHT, padx=15)

        show_user_movies_btn = ttk.Button(
            master=term_row, 
            text="Show user's movies", 
            command=self.show_users_movies,
            bootstyle=OUTLINE, 
            width=18
        )
        show_user_movies_btn.pack(side=RIGHT, padx=15)

    def create_results_view(self):
        """Add result treeview to labelframe"""
        self.resultview = ttk.Treeview(
            master=self, 
            bootstyle=INFO, 
            columns=[0, 1, 2, 3, 4, 5],
            show=HEADINGS
        )
        self.resultview.pack(fill=BOTH, expand=YES, pady=5)

        # setup columns and use `scale_size` to adjust for resolution
        self.resultview.heading(0, text='', anchor=W)
        self.resultview.heading(1, text='Title', anchor=W)
        self.resultview.heading(2, text='Year', anchor=W)
        self.resultview.heading(3, text='Rating', anchor=W)
        self.resultview.heading(4, text='Votes', anchor=W)
        self.resultview.column(
            column=0, 
            anchor=W, 
            width=utility.scale_size(self, 50), 
            stretch=False
        )
        self.resultview.column(
            column=1, 
            anchor=W, 
            width=utility.scale_size(self, 300), 
            stretch=False
        )
        self.resultview.column(
            column=2, 
            anchor=W, 
            width=utility.scale_size(self, 130), 
        )
        self.resultview.column(
            column=3, 
            anchor=W, 
            width=utility.scale_size(self, 130), 

        )
        self.resultview.column(
            column=4, 
            anchor=W, 
            width=utility.scale_size(self, 120)
        )

    def add_user_entry(self):
        path_user = (pathlib.Path(__file__) / '..'/'..').resolve()/"data/app_users.csv"
        rating = self.rating.get()
        user_id = self.user_id.get()
        movie_title = self.movie_title.get()
        item = self._data_movies.query(f"title == '{movie_title}'").index[0]
        new_entry = pd.DataFrame({"user":[user_id], "item":[item], "rating":[rating]}, index=[self._last_index + 1])
        new_entry.to_csv(path_user, mode="a", header=False) 
        self._last_index += 1
        self._data_users = pd.read_csv(path_user, index_col=0)

    def get_user_movies(self, user_id):
        movies = self._data_users.query(f"user == {user_id}")
        return movies

    def show_users_movies(self):
        user_id = self.user_id.get()
        movies = self.get_user_movies(user_id)
        children = self.resultview.get_children()
        if children != ():
            self.resultview.delete(*children)

        movies = movies.join(self._data_movies.title, on="item").join(self._data_links.drop(columns=["imdbId"]), on="item")

        for index_, row  in enumerate(movies.values): 
            rank = index_ + 1
            title = row[3]
            score = row[2]
            release_year = row[4]
            runtime = row[5]
            votes = int(row[6])
            iid = self.resultview.insert(
                    parent='', 
                    index=END, 
                    values=(rank, title, release_year, score, runtime, votes)
                )




def main():
    app = ttk.Window("NaSC", themename="cyborg")
    
    path = (pathlib.Path(__file__) / '..'/'..').resolve()
    algorithms   = path/"data/models/"
    data_movies_path = str(path/"data/ml-100k/movies.csv")
    data_users_path = str(path/"data/app_users.csv")
    data_links_path = str(path/"data/ml-100k/links.csv")

    data_movies = pd.read_csv(data_movies_path, index_col=0)
    data_users = pd.read_csv(data_users_path, index_col=0)
    data_links = pd.read_csv(data_links_path, index_col=0)
    RecommenderEngine(app, algorithms, data_movies, data_users, data_links)
    app.mainloop()

if __name__ == '__main__':
    main()