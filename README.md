SalesPrediction
===============
Predict sales by analyzing social network data.

Install
===============
The code is implemented using **Python 3**. You also need to install [BeautifulSoup][beautifulSoup] and [Twython][twython]:

`$ pip install beautifulsoup4`

`$ pip install twython`

Get Started
===============
##Get data from twitter
You need a text file that list all the account you want to fetch. A sample file `sample_list.txt` looks like:

```
id_1
id_2
id_3
...
```
Then use `fetch_twitter.py` to get data and save to file:

`$ python fetch_twitter.py sample_list.txt`

##Run the pipeline

After fetching data from twitter, you can run the pipeline with one argument indicating the path to the directory of data files:

`$ python pipeline.py ./data`

As most of the work is network I/O intensive, it's better to do parallel computing. We do use multiple processes when searching eaby. However, we don't have time to implement the main logic for each tweets in parallel. Instead, you can divide the twitter data into several sets, like `./data1`, `./data2`, `./data3`, ... . Then you can open several terminals and process each set concurrently.

[beautifulSoup]:http://beautiful-soup-4.readthedocs.org/en/latest/#
[twython]:https://twython.readthedocs.org/en/latest/
