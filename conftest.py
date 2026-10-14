"""Shared pytest configuration and fixtures for the decay project."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent
DATA_FILE = REPO_ROOT / "data" / "decay_counts.csv"


@pytest.fixture(scope="session")
def data_file():
    """Absolute path to the bundled decay-counts CSV.

    Uses a path relative to this file, not the working directory, so tests
    pass whether you run pytest from the repo root, from tests/, or in CI.
    """
    assert DATA_FILE.exists(), f"missing data file: {DATA_FILE}"
    return DATA_FILE


@pytest.fixture
def clean_decay():
    """Noiseless synthetic decay data with lambda = 0.35 / yr."""
    import numpy as np

    t = np.arange(0, 10, 0.5)
    counts = 1000 * np.exp(-0.35 * t)
    return t, counts
