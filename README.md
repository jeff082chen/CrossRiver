# Cross River
人工智慧期末專題
  
# how to use
``` zsh
# clone the project
$ git clone git@github.com:jeff082chen/CrossRiver.git

$ cd CrossRiver

# arguments
# -N: integer between 3~10
# -M: integer between 0~2
# -l: limit of cost (time limit if -p, price limit if -t) (default: no limit)
# -d: debug mode
# algorithm: -UC -> UniformCost, -AS -> A*
# mode: -p -> minimum price, -t -> minimun time
$ python -m CrossRiver.main -N[3..10] -M[0..2] [-t or -p] [-UC or -AS] [-d] [-l[limit]]
```
