import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

AVG_N = 5

def csv_to_df(file, transpose = False, avg = True):
    """
    Converts row based csv to a dataframe.
    e.g. first element of row is info, rest are info about it.
    TODO maybe do transpose version
    :param file:
    :return:
    """
    out = []
    with open(file) as csvfile:
        rdr = csv.reader(csvfile)
        for row in rdr:
            print(len(row))
            if(row[-1]==''):
                row = row[0:-1]

            r = [int(x) for x in row]
            if(avg):
                r = [r[0]] + [np.mean(r[x:x+5]) for x in range(1,len(r)-5, 5)]

            out.append(r)
    out = np.array(out)
    df = pd.DataFrame({'x':range(0,len(out[1,])-1)})
    for i in range(0,len(out)):
        df[out[i][0]] = out[i][1:]
    #print(df)
    return df

df_rf = csv_to_df("rdata_rel_false.csv")
df_rt = csv_to_df("rdata_rel_true.csv")

print(df_rt.shape)
print(df_rf.shape)

print(df_rt)
print(df_rf.shape)



plt.plot(df_rf['x'], df_rf[1], color = 'blue')
plt.plot(df_rt['x'], df_rt[1], color='red')

# plt.plot(df_rf['x'], df_rf[3], color = 'green')
# plt.plot(df_rt['x'], df_rt[3], color='brown')

# plt.plot('x', 'n1', data=df, color='blue')
# plt.plot([rw_per_arm[0] for x in range(0,len(out[1,]))], color = 'blue')
#
# plt.plot('x', 'n3', data=df, color='red')
# plt.plot([rw_per_arm[2] for x in range(0,len(out[1,]))], color = 'red')
# #plt.plot('x', 'n4', data=df, color='green')
# #plt.plot('x', 'n5', data=df, color='orange')
# #plt.plot('x', 'n6', data=df, color='brown')
# plt.plot('x', 'n8', data=df, color='brown')
# plt.plot([rw_per_arm[7] for x in range(0,len(out[1,]))], color = 'brown')
# #plt.plot('x', 'n8', data=df, color='red')
# #plt.plot('x', 'n7', data=df, color='brown')
# # plt.plot('x', 'n10', data=df, color='green')
# # plt.plot('x', 'n15', data=df, color='red')
# #plt.plot('x', 'n9', data=df, color='brown')
# plt.legend()

plt.xlabel("Avg reward over " + str(AVG_N) + " episodes" )
plt.ylabel("reward")
plt.title("Average reward per 5 episodes N-jointed effector")
plt.show()


