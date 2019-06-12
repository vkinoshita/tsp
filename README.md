# TSP
This project solves the Travelling Salesman Problem by many methods: brute force, greedy algorithm, 3-opt by simulation and integer programming.

## Dependencies

The project code is based on python 3.7. 
To install all dependencies, make sure that you have pip installed. 
If you are in an Windows environment, installing Anaconda can help you with some errors while trying to install some libraries.

After you setup everything, just run `$ pip install -r requirements.txt`.

## How to run the algorithms

In the project root, the base command is:

```bash
$ python main.py <options>
```

You can setup many options to solve the TSP:

| Options | Description |
| - | - |
|`-r <n>` or `--rand-size <n>` | `n` is desired points in the graph randomly generated. |
|`-p` or `--plot` | Pops up a window showing a plotted solution. |
|`-f <file-name>` or `--plot-to-file <file-name>` | Saves the plotted solution to a `file-name` |
|`-s <solver-name>` or `--solver <solver-name>` | You can use the following `solver-name`: `brute-force`, `greedy`, `mip`, `mip-s`, `mip-s-2`, `3-opt`. |
|`-b <n1> <n2> <n3>` or `--benchmark <n1> <n2> <n3>` | From `n1` points randomly generated to `n2` points randomly generated, repeating `n3` times each. |
|`-z <file-name>` or `--benchmark-file <file-name>` | Saves the benchmark, described above, to a `file-name`. |

If you does not have [Gurobi](https://python-mip.readthedocs.io/en/latest/install.html) installed, look for `model = Model(solver_name='gurobi')` in `mip.py` and change each one of them to `model = Model(solver_name='cbc')`. I'm too lazy to make a conditional to use CBC or Gurobi.

Examples:

```bash
$ python main.py --solver mip-s --benchmark 10 200 1 --benchmark-file mip.csv

$ python main.py --solver 3-opt --benchmark 803 1000 1 --benchmark-file 3_opt_2.csv

$ python main.py --solver brute-force --rand-size 10 --plot

$ python main.py --solver greedy --plot --plot-to-file images/greedy/2.png
```

Feel free to read or change the code by yourself, it's pretty simple.