import argparse



parser = argparse.ArgumentParser()
parser.add_argument('--steps', type=int)
parser.add_argument('--1reward', dest='reward', action='store_true')
parser.add_argument('--goals', type = int)


args = parser.parse_args()
print(args.steps)
print(args.reward)
print(args.goals)

