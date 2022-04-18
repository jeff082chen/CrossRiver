# Cross River
人工智慧期末專題
  
# how to use
``` zsh
# clone the project
$ git clone git@github.com:jeff082chen/CrossRiver.git

$ cd CrossRiver

$ pip install -r requirements.txt

# arguments
# -N: integer between 3~10
# -M: integer between 0~2
# -m mode: 0 -> minimum price, 1 -> minimun time
# -a algorithm: UC -> UniformCost, AS -> A*
$ python -m CrossRiver.main -N[3..10] -M[0..2] -m[0..1] -a[alg]
```
