import argparse
import pickle
parser = argparse.ArgumentParser()
parser.add_argument('-f')
args = parser.parse_args()
variables_file = args.f

variables = {"1589795877": ["doge", "53"]}
with open(variables_file, 'wb') as f:
    pickle.dump(variables, f)

with open(variables_file, 'rb') as f:
    variables = pickle.load(f)

print(variables)
