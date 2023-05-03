# Coronavirus twitter analysis

In this project, I scanned all geotagged tweets sent in 2020 to monitor for the spread of the coronavirus on social media.

**Objectives:**

1. work with large scale datasets
1. work with multilingual text
1. use the MapReduce divide-and-conquer paradigm to create parallel code

## Background

**About the Data:**

Approximately 500 million tweets are sent everyday.
Of those tweets, about 2% are *geotagged*.
That is, the user's device includes location information about where the tweets were sent from.
In total, there were about 1.1 billion tweets in the dataset I analyzed.

**About MapReduce:**

I followed the [MapReduce](https://en.wikipedia.org/wiki/MapReduce) procedure to analyze these tweets.
MapReduce is a famous procedure for large scale parallel processing that is widely used in industry.
It is a 3 step procedure summarized in the following image:

<img src=mapreduce.png width=100% />

**MapReduce Runtime:**

Let $n$ be the size of the dataset and $p$ be the number of processors used to do the computation.
The simplest and most common scenario is that the map procedure takes time $O(n)$ and the reduce procedure takes time $O(1)$.
(These were the runtimes of my map/reduce procedures.)
In this case, the overall runtime was $O(n/p + \log p)$.
In the typical case when $p$ is much smaller than $n$,
then the runtime simplifies to $O(n/p)$.
This means that:
1. doubling the amount of data will cause the analysis to take twice as long;
1. doubling the number of processors will cause the analysis to take half as long;
1. if you want to add more data and keep the processing time the same, then you need to add a proportional number of processors.

## Programming Tasks

I followed the procedure below:

**Step 0: Create the mapper**

I created a the `map.py` file so that it tracks the usage of the hashtags on both a language and country level.
For this, I created two variables called `counter_country` and `counter_lang`, 
and the output of running `map.py` was two files, one that ended in `.lang` for the language dictionary,
and one that ended in `.country` for the country dictionary.

**Step 1: Run the mapper**

I created a shell script called `run_maps.sh`.
This file looped over each file in the dataset and run the `map.py` command on that file.
Each call to `map.py` could take up to a day to finish, so I used the `nohup` command to ensure the program continued to run after I disconnected and I also used the `&` 
operator to ensure that all `map.py` commands ran in parallel.
```
$ ./src/map.py --input_path=/data/Twitter\ dataset/geoTwitter*.zip
```

**Step 2: Reduce**

After my `map.py` had run on all the files,
I now had a large number of files in my `outputs` folder.
I then used the `reduce.py` file to combine all of the `.lang` files into a single file,
and all of the `.country` files into a different file.
```
$ ./src/reduce.py --input_paths outputs/geoTwitter*.lang --output_path=reduced.lang
```
```
$ ./src/reduce.py --input_paths outputs/geoTwitter*.country --output_path=reduced.country
```

**Step 3: Visualize**

To visualize my output files I used the command
```
$ ./src/visualize.py --input_path=PATH --key=HASHTAG
```

My `visualize.py` file generated a bar graph of the results and stored the bar graph as a png file.
The horizontal axis of the graph was the keys of the input file,
and the vertical axis of the graph was the values of the input file.
I filtered the final results include only the top 10 keys and were sorted from low to high.

I then, ran the `visualize.py` file with the `--input_path` equal to both the country and lang files created in the reduce phase, and the `--key` set to `#coronavirus` and `#코로나바이러스`.
The plots generated are below.

Language Ranks for  #코로나바이러스

<img src=LanguageKorean.png width=50% />

Country ranks for #코로나바이러스

<img src=CountryKorean.png width=50% />

Language ranks for #coronavirus

<img src=LanguageEnglish.png width=50% />

Country ranks for #coronavirus

<img src=CountryEnglish.png width=50% />

**Step 4: Alternative Reduce**

I also then created a new file called `alternative_reduce.py`.
This fil took as input on the command line a list of hashtags,
and outputed a line plot where:
1. There was one line per input hashtag.
1. The x-axis was the day of the year.
1. The y-axis was the number of tweets that used that hashtag during the year.

The `alternative_reduce.py` file followed a similar structure to a combined version of the `reduce.py` and `visualize.py` files.
First, I scanned through all of the data in the `outputs` folder created by the mapping step.
In this scan, constructed a dataset that contained the information that I needed to plot.
Then, after I had extracted this information,
I called on a matplotlib functions to plot the data and got the graph below.

Alternative_Reduce

<img src=alternative_reduce_plot2.png width=50% />
