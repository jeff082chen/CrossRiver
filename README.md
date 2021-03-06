# Cross River
人工智慧期末專題
  
# how to use
``` zsh
# clone the project
$ git clone git@github.com:jeff082chen/CrossRiver.git

$ cd CrossRiver

# install dependencies
$ pip install -r requirements.txt

# GUI app
$ python -m GUI

# Command line interface
$ python -m CrossRiver --help
```

# CLI
```
usage: CrossRiver [-h] [--debug] [--limit lim] (--time | --price) (-AS | -UC)
                  {3,4,5,6,7,8,9,10} {0,1,2}

Missionaries and Cannibals Problem

positional arguments:
  {3,4,5,6,7,8,9,10}   N: integer between 3 and 10
  {0,1,2}              M: integer between 0 and 2

optional arguments:
  -h, --help           show this help message and exit
  --debug, -d          debug mode
  --limit lim, -l lim  limit: price limit when mode is time, and vice versa
  --time, -t           mode: time
  --price, -p          mode: price
  -AS                  A* Search
  -UC                  Uniform Cost
```

# GUI app
<img src="https://github.com/jeff082chen/CrossRiver/blob/main/img/app.png" width="500"/>  

1. input parameters 
    + N: integer between 3~10
    + M: integer between 0~2
    + limit: limit of cost (time limit if -p, price limit if -t) (default: no limit)
    + mode: price (p for short) or time (t for short)
2. press `search` button
3. wait until label shows `ready to move`
4. press `next` button to move, press `prev` button go back to previous step
5. press `auto` button to finish the game automatically
6. when label shows `ready to reset`, press `reset` button
7. press `quit` button to quit, or press `search` button to restart
