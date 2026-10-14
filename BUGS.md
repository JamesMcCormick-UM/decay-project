# Bug log
---

## Template

## Bug N — [loud | intermittent | silent]
**Symptom:** what was observed (error text, or wrong value vs. expected 1.98 yr)
**Root cause:** file + line, and why that line was wrong
**Fix:** what changed
**How it was found:** traceback / pdb / assertion / logging / compared to expected
**Regression test:** `tests/test_decay_lab.py::test_name`

---

## Bug 1 — silent (example)
**Symptom:** half-life reported as 1.9790 yr instead of 1.9804 yr (0.07% low).
**Root cause:** `decay_lab.py` — `DAYS_PER_YEAR = 365` instead of `365.25`.
**Fix:** restored the Julian year.
**How it was found:** compared against the known answer for the bundled data.
**Regression test:** `tests/test_decay_lab.py::test_time_axis_uses_julian_year`
