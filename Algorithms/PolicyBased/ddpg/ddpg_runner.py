import os

for i in range(1,10,2):
    os.system("python ddpg_njoints_nm.py " + str(i))
    print("complete")