
# Introduction
This a learning evolution on how one can speed up basic I/O such as socket
connections by using Python 3.7.

Let's define our data set first. For this exercise I picked up the Top 1M
visited websites. This is a report by Amazon and can be found [here](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip).

We basically want to open a socket connection on every domain on port 443 and
check whether it is open or not.

For the sake of this exercise I'm going to get only the first 100 endpoints.

Let's start by the most simplistic way: `socket_sync.py`

```
$ time python socket_sync.py
Opening socket to google.com
Done socket on google.com with result Open
Opening socket to youtube.com
Done socket on youtube.com with result Open
Opening socket to facebook.com
Done socket on facebook.com with result Open
Opening socket to baidu.com
Done socket on baidu.com with result Open
Opening socket to wikipedia.org
Done socket on wikipedia.org with result Open
Opening socket to reddit.com
Done socket on reddit.com with result Open
Opening socket to yahoo.com
Done socket on yahoo.com with result Open

Endpoints took 22.2828311920166 seconds
```

What about multiprocessing?: `socket_multiprocessing.py`

```
# Using 10 processes
$ time python socket_multiprocessing.py

Endpoints took 12.603057146072388 seconds

```

Now let's try `concurrent.futures` with a `ThreadPoolExecutor`

```
# Using 10 threads
$ time python socket_futures.py

Endpoints took 3.016674041748047 seconds
```

Finally let's use `asyncio`: `socket_asyncio.py`

Notice how the endpoints that timeout are at the end. The idea here is that this
code is more efficient resource wise because we don't rely on the OS scheduler
> There is a lot of room for improvement so the take away here is not the actual runtime.

```
$ time python socket_async.py
Opening socket to google.com
Opening socket to youtube.com
Opening socket to facebook.com
Opening socket to baidu.com
Opening socket to wikipedia.org
Opening socket to reddit.com
Opening socket to yahoo.com
Opening socket to qq.com
Opening socket to taobao.com
...
...
...
Done socket on tianya.cn with result Open
Done socket on so.com with result Open
Done socket on detail.tmall.com with result Open
Done socket on sina.com.cn with result Open
Done socket on 360.cn with result Open
Done socket on qq.com with result Timeout
Done socket on microsoftonline.com with result Timeout
Done socket on alipay.com with result Timeout
Done socket on k618.cn with result Timeout

Endpoints took 5.620862007141113 seconds
```
