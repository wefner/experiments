
# Introduction
This a learning evolution on how one can speed up basic I/O such as socket
connections by using Python 3.6+

Let's define our data set first. For this exercise I picked up the Top 1M
visited websites. This is a report by Amazon and can be found [here](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip).

We basically want to open a socket connection on every website on port 443 and
check whether it is open or not.

For the sake of this exercise I'm not going to test 1M websites but a sample of 1000.

There is a chart image in this repo as well.

Let's start by the most simplistic way: `socket_sync.py`

```
$ time python socket_sync.py
Testing endpoint google.com
Endpoint google.com result: Open
Testing endpoint youtube.com
Endpoint youtube.com result: Open
Testing endpoint facebook.com
Endpoint facebook.com result: Open
Testing endpoint baidu.com
Endpoint baidu.com result: Open
Testing endpoint wikipedia.org
Endpoint wikipedia.org result: Open
Testing endpoint reddit.com
Endpoint reddit.com result: Open
Testing endpoint yahoo.com
Endpoint yahoo.com result: Open
Testing endpoint qq.com
Endpoint qq.com result: Timeout
Testing endpoint taobao.com
Endpoint taobao.com result: Open
Testing endpoint twitter.com
Endpoint twitter.com result: Open

real	3m20.602s
```

Average of 5 runs: 207 seconds (3m45s)

Now let's use `asyncio`: `socket_asyncio.py`

Notice how the endpoints that timeout are at the end. We gain some speed as we
don't wait for endpoints to timeout but we carry onto the next one.
```
$ time python socket_async.py
Testing endpoint youtube.com
Endpoint youtube.com result: Open
Testing endpoint reddit.com
Endpoint reddit.com result: Open
Testing endpoint yahoo.com
Endpoint yahoo.com result: Open
Testing endpoint qq.com
Testing endpoint facebook.com
Endpoint facebook.com result: Open
Testing endpoint taobao.com
Endpoint taobao.com result: Open
Testing endpoint baidu.com
Endpoint baidu.com result: Open
Testing endpoint twitter.com
Endpoint twitter.com result: Open
Testing endpoint google.com
Endpoint google.com result: Open
Testing endpoint wikipedia.org
Endpoint wikipedia.org result: Open
Endpoint qq.com result: Timeout

real	3m02.0316s
```
Average of 5 runs: 183 seconds (3m05s)

What about multiprocessing?: `socket_multiprocessing.py`

```
# Using 10 processes
$ time python socket_multiprocessing.py

real	1m46.026s
```
Average of 5 runs: 108 seconds (1m48s)

```
# Using 100 processes
$ time python socket_multiprocessing.py

real	0m21.617s
```
Average of 5 runs: 29 seconds

And finally, let's try `concurrent.futures`

```
# Using 10 threads
$ time python socket_futures.py

real	0m19.827s
```
Average of 5 runs: 19 seconds

```
# Using 100 threads
$ time python socket_futures.py

real	0m5.128s
```
Average of 5 runs: 5 seconds

