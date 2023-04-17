
# Introduction
This a learning evolution on how one can speed up basic I/O such as multiple HTTP request
connections by using Python.

Let's define our data set first. For this exercise I picked up the Top 1M
visited websites. This is a report by Amazon and can be found [here](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip).

We basically want to crate a `GET` HTTP request to every website in the list.

For the sake of this exercise I'm going to get only up to the first 1000 endpoints.

# Runs
Let's start by the most simplistic way:

```
$ python socket_sync.py
10 endpoints took 3.12 seconds
100 endpoints took 41.84 seconds
500 endpoints took 317.75 seconds
1000 endpoints took 642.83 seconds
```

What about multiprocessing?

```
# Using 8 processes
$ python socket_multiprocessing.py
10 endpoints took 0.95 seconds
100 endpoints took 8.68 seconds
500 endpoints took 52.82 seconds
1000 endpoints took 86.07 seconds
```

Now let's try `concurrent.futures` with a `ThreadPoolExecutor`.

```
$ python socket_futures.py
10 endpoints took 0.83 seconds
100 endpoints took 6.06 seconds
500 endpoints took 34.15 seconds
1000 endpoints took 75.72 seconds
```

Finally, let's use `asyncio`:

The idea here is that this code is more efficient resource wise because we don't rely on the OS scheduler.

```
$ python socket_asyncio.py
10 endpoints took 1.46 seconds
100 endpoints took 3.15 seconds
500 endpoints took 16.91 seconds
1000 endpoints took 57.64 seconds
```
