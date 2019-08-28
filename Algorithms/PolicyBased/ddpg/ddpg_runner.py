import os

for i in range(10,15):
    os.system("python ddpg_njoints_nm.py " + str(i))
    print("complete")