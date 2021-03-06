from demo import cache
import glob
import os
import itertools
import json
import numpy as np
from collections import defaultdict

class Analyzer:
    def __init__(self):
        results_dir = os.path.join(os.path.dirname(__file__),
                "data", "results", "run")
        files = map(os.path.basename, glob.glob(os.path.join(results_dir,
            "*.json")))
        self.estimates = defaultdict(dict)
        self.distances = {}
        self.errors = defaultdict(dict)
        self.abs_errors = defaultdict(dict)
        self.corrected = defaultdict(dict)

        with open(os.path.join(results_dir, files[0])) as sample:
            self.keys = json.load(sample).keys()

        for key in self.keys:
            for N in range(1, 41):
                self.estimates[key][N] = {}
                self.errors[key][N] = {}
                self.abs_errors[key][N] = {}
                self.corrected[key][N] = {}
            self.distances[key] = cache.cache[key]
       
        for file in files:
            _, N, C = file.split(".")[0].split("_")
            N = int(N)
            C = int(C)
            with open(os.path.join(results_dir, file)) as datafile:
                data = json.load(datafile)
                for key in self.keys:
                    self.estimates[key][N][C] = data[key]
                    error = (data[key] - self.distances[key]) \
                            / float(self.distances[key])
                    self.errors[key][N][C] = error
                    self.abs_errors[key][N][C] = abs(error)
                    self.corrected[key][N][C] = abs((data[key]*0.8291 - self.distances[key]) / float(self.distances[key]))

    def stats(self, N=None, C=None, corrected=False):
        if N == None:
            N = range(1,41)
        try:
            iter(N)
        except:
            N = range(N, N+1)
        if C == None:
            C = range(100, 201, 10)
        try:
            iter(C)
        except:
            C = range(C, C+1)
    
        errors = []
        for key in self.keys:
            for n in N:
                for c in C:
                    if corrected:
                        errors.append(self.corrected[key][n][c])
                    else:
                        errors.append(self.abs_errors[key][n][c])

        return {"min":min(errors), "max":max(errors),
                "average":np.mean(errors), "stddev":np.std(errors)}

    def n_list(self, corrected=False):
        Ns = []
        for N in range(1, 41):
            Ns.append((N, self.stats(N=N, corrected=corrected)["average"]))
        return sorted(Ns, key=lambda x: x[1])

analyzer = Analyzer()
print analyzer.stats()
for line in analyzer.n_list():
    print line
