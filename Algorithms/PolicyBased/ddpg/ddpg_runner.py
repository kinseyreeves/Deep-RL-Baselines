import os

for i in range(0,10):
    os.system("python ddpg_njoints_nm.py " + str(i))
    print("complete")