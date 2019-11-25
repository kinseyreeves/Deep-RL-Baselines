import csv
import matplotlib.pyplot as plt

tests = [1,3]

def get_first_col(filename):
    f = open(filename, "r")
    steps = []
    for line in f:
        if (len(line) == 1):
            continue
        line = line.strip("\n").split(",")
        step = int(line[0])
        steps.append(step)

    return steps

_1j_ddpg = get_first_col("baseline/eval_res_1.txt")
_3j_ddpg = get_first_col("baseline/eval_res_3.txt")

_1j_jac = get_first_col("baseline/results_1.txt")
_3j_jac = get_first_col("baseline/results_2.txt")

data = [_1j_ddpg, _3j_ddpg, _1j_jac, _3j_jac]
labels = ["1J DDPG", "3J DDPG", "1J JACOBIAN", "3J JACOBIAN"]

boxplot = plt.boxplot(data, labels = labels)
plt.ylabel("Steps taken to goal")
plt.title("Steps taken to goal over 100 episodes")
plt.show()