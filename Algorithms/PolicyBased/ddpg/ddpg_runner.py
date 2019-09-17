import os

for i in range(0,11,2):
    os.system("python ddpg_njoints_nm.py " + str(i))
    print("complete")