import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

AVG_N = 5

out = []
with open("rdata.csv") as csvfile:
    rdr = csv.reader(csvfile)
    for row in rdr:
        inner = []
        for i in range(0,len(row),AVG_N):
            ele = [int(x) for x in row[i:i+5]]
            inner.append(int(np.mean(ele)))
        #print(len(inner))
        out.append(inner)

rw_per_arm = []
steps_per_arm = []

for i in range(1,9):
    f = open(f"baseline/results_{i}.txt", "r")
    all_steps = []
    all_rew = []
    for line in f:
        l = line.strip("\n").split(",")
        print(l)
        if(len(l)==1):
            continue
        all_steps.append(int(l[0]))
        all_rew.append(float(l[1]))
    print(all_rew)
    rw_per_arm.append(np.mean(all_rew))
    steps_per_arm.append(np.mean(all_steps))


# print(rw_per_arm)
# print(steps_per_arm)
# exit(0)
out = np.array(out)
rewards = out[:,1:]
print(rewards[0])


df = pd.DataFrame({'x':range(0,len(out[1,])), 'n1':out[1,], 'n2':out[2,], 'n3':out[3,], 'n4':out[4,],
                   'n5':out[5,], 'n6':out[6,], 'n7':out[7,], 'n8':out[8,], 'n9':out[9,], 'n10':out[10,],
                   'n11':out[11,], 'n12':out[12,], 'n13':out[13,], 'n14':out[14,], 'n15':out[15,]})

joints = out[:,0]

#plt.plot('x', 'n2', data=df, color='blue')
plt.plot('x', 'n1', data=df, color='blue')
plt.plot([rw_per_arm[0] for x in range(0,len(out[1,]))], color = 'blue')

plt.plot('x', 'n3', data=df, color='red')
plt.plot([rw_per_arm[2] for x in range(0,len(out[1,]))], color = 'red')
#plt.plot('x', 'n4', data=df, color='green')
#plt.plot('x', 'n5', data=df, color='orange')
#plt.plot('x', 'n6', data=df, color='brown')
plt.plot('x', 'n8', data=df, color='brown')
plt.plot([rw_per_arm[7] for x in range(0,len(out[1,]))], color = 'brown')
#plt.plot('x', 'n8', data=df, color='red')
#plt.plot('x', 'n7', data=df, color='brown')
# plt.plot('x', 'n10', data=df, color='green')
# plt.plot('x', 'n15', data=df, color='red')
#plt.plot('x', 'n9', data=df, color='brown')
plt.legend()

plt.xlabel("Avg reward over " + str(AVG_N) + " episodes" )
plt.ylabel("reward")
plt.title("Average reward per 5 episodes N-jointed effector")
plt.show()

print(rewards)

