# NaSC (Name Subject to Change) Recommender

Here we have a simple interface to visually test some recommendation algorithms from [lenskit](https://lkpy.readthedocs.io/en/stable/index.html). The main reason I built this project was so I could work with some of the subjects I recently got interested in.

<p align="center" width="100%">
<img src="https://user-images.githubusercontent.com/76168138/165192123-5e97bd21-c898-410d-b52f-4897254471ab.png" width="672" height="421"/>
</p>

To get your recommendations, click on Add user/movie, type a number as your user id e search the name of the movies you watched and their ratings (0.5 to 5), then go back to the initial window, fill in the form and choose any of the available trained models.

If you want to use your model check out the Jupyter Notebook on data/ to see examples of how to do so.

Disclaimer: All the predicted ratings are relative to a certain configuration (biases and model) and cannot be compared to items outside of the said configuration.
