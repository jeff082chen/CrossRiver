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
$ python -m GUI.app

# Command line interface
$ python -m CrossRiver.main --help
```

# GUI app
<img src="https://github.com/jeff082chen/CrossRiver/blob/main/img/app.png" width="500"/>  

1. input parameters 
    + N: integer between 3~10
    + M: integer between 0~2
    + limit: limit of cost (time limit if -p, price limit if -t) (default: no limit)
    + mode: price (p for short) or time (t for short)
2. press `search` button
3. when label shows `ready to move`, press `move` button
4. wait for the move to finish
5. when label shows `ready to reset`, press `reset` button
6. press `quit` button to quit, or press `search` button to restart
