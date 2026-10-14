# Decay Project — COMPFOR 203

Estimates a radioisotope half-life from decay counts by fitting
`ln(N) = ln(N0) - lambda*t`, then bootstraps a 95% confidence interval.

**Expected answer on the bundled data: half-life ≈ 1.98 yr** (true lambda = 0.35 / yr).

## Setup
```bash
mamba env create -f environment.yml
#you need to install mamba if you dont have it, https://github.com/conda-forge/miniforge
mamba activate compfor203
pre-commit install
```
##RUN
python decay_lab.py data/decay_counts.csv
python decay_lab.py data/decay_counts.csv --log-level DEBUG

##TEST
pytest                 # all tests
pytest -x              # stop at first failure
pytest --lf            # only what failed last time
pytest -k property     # only tests matching "property"

##Layout
decay_lab.py           #the analysis
data/decay_counts.csv  #synthetic counts, 21 points over 8 years
tests/                 #pytest suite
conftest.py            #shared fixtures (data_file, clean_decay)
BUGS.md                #bug log — symptom, root cause, fix, regression test
