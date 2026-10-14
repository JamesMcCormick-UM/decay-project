# written with the help of Claude Opus 5, James McCormick 2026.

"""Estimate a radioisotope half-life from decay counts.

Model:  N(t) = N0 * exp(-lambda * t)   =>   ln N = ln N0 - lambda * t
Fits a log-linear regression, then bootstraps a 95% CI on the half-life.

Usage:
    python decay_lab.py data/decay_counts.csv
    python decay_lab.py data/decay_counts.csv --log-level DEBUG
"""

from __future__ import annotations

import argparse
import logging
import sys

import numpy as np
import pandas as pd

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
DAYS_PER_YEAR = 365.25
SEED = 20261021
N_BOOTSTRAP = 2000

log = logging.getLogger("decay")


def load_counts(path):
    """Read a CSV with columns time_days, counts. Return (t_years, counts)."""
    df = pd.read_csv(path)
    required = {"time_days", "counts"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")

    df = df.sort_values("time_days").reset_index(drop=True)
    t_years = df["time_days"].to_numpy(dtype=float) / DAYS_PER_YEAR
    counts = df["counts"].to_numpy(dtype=float)

    log.info("loaded %d rows from %s", len(df), path)
    log.debug("t range: %.3f to %.3f yr", t_years.min(), t_years.max())
    return t_years, counts


def decay_constant(t, counts):
    """Fit ln(N) = ln(N0) - lambda*t and return lambda in 1/yr."""
    assert t.shape == counts.shape, f"shape mismatch: {t.shape} vs {counts.shape}"

    mask = counts > 0
    if mask.sum() < 3:
        raise ValueError(f"need >= 3 nonzero counts to fit, got {mask.sum()}")
    if not mask.all():
        log.warning("dropped %d zero-count rows", int((~mask).sum()))

    slope, intercept = np.polyfit(t[mask], np.log(counts[mask]), 1)
    log.debug("slope=%.6f intercept=%.6f", slope, intercept)
    return -slope


def half_life(lmbda):
    """Convert a decay constant (1/yr) to a half-life (yr)."""
    assert lmbda > 0, f"non-physical decay constant: {lmbda:.4g}/yr"
    return np.log(2.0) / lmbda


def bootstrap_half_life(t, counts, rng, n=N_BOOTSTRAP):
    """Resample points with replacement; return n half-life estimates."""
    idx = np.arange(len(t))
    out = np.empty(n)
    for i in range(n):
        pick = rng.choice(idx, size=len(idx), replace=True)
        out[i] = half_life(decay_constant(t[pick], counts[pick]))
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Estimate a half-life from decay counts.")
    p.add_argument("csv", help="input CSV with time_days, counts")
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = p.parse_args(argv)

    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    log.info("seed=%d numpy=%s pandas=%s", args.seed, np.__version__, pd.__version__)

    t, counts = load_counts(args.csv)
    assert np.all(np.diff(t) > 0), "time_days must be strictly increasing"
    assert np.all(counts >= 0), "counts cannot be negative"

    lam = decay_constant(t, counts)
    hl = half_life(lam)

    rng = np.random.default_rng(args.seed)
    boot = bootstrap_half_life(t, counts, rng)
    lo, hi = np.percentile(boot, [2.5, 97.5])

    print(f"lambda      = {lam:.4f} / yr")
    print(f"half-life   = {hl:.4f} yr")
    print(f"95% CI      = [{lo:.4f}, {hi:.4f}] yr")
    return 0


if __name__ == "__main__":
    sys.exit(main())
