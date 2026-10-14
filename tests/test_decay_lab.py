import numpy as np
import pytest

from decay_lab import decay_constant, half_life, load_counts


def test_half_life_of_known_lambda():
    # lambda = ln2 => half-life = exactly 1
    assert half_life(np.log(2)) == 1.0


def test_recovers_known_lambda_from_clean_data():
    t = np.arange(0, 10, 0.5)
    counts = 1000 * np.exp(-0.35 * t)
    assert decay_constant(t, counts) == 0.35


# pytest.approx()


def test_rejects_nonphysical_lambda():
    with pytest.raises(AssertionError):
        half_life(-0.35)


def test_too_few_points_raises():
    with pytest.raises(ValueError, match="need >= 3"):
        decay_constant(np.array([0.0, 1.0]), np.array([100.0, 50.0]))


def test_missing_column_raises(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("time_days,oops\n0,100\n")
    with pytest.raises(ValueError, match="missing columns"):
        load_counts(bad)


def test_time_axis_uses_julian_year(data_file):  # data_file comes from conftest.py
    """Regression: BUGS.md #2 — DAYS_PER_YEAR was 365, biasing λ by 0.07%."""
    t, _ = load_counts(data_file)
    assert t[-1] == pytest.approx(2920 / 365.25, rel=1e-12)
