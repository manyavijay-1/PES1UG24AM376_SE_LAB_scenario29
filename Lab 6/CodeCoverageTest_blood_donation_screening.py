"""
Lab 6 - Part 1: LINE coverage tests for blood_donation_screening.py

Run (from the "Lab 6" folder):
    coverage run -m pytest CodeCoverageTest_blood_donation_screening.py
    coverage report -m
"""

import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge

VOLUME = 450


def make_cohort(donors, registered=True, cohort_type="standard", fast_track=False):
    """Small helper so each test only states what it cares about."""
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


GOOD_DONOR = {"age": 25, "weight_kg": 65, "hb": 14.0}


# ---------------------------------------------------------------------------
# process_donor_cohort
# ---------------------------------------------------------------------------
def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([GOOD_DONOR])], VOLUME)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_cohort_type_raises():
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", VOLUME)


def test_non_positive_volume_raises():
    with pytest.raises(ValueError):
        process_donor_cohort([make_cohort([GOOD_DONOR])], 0)


def test_unregistered_clinic_is_skipped():
    result = process_donor_cohort([make_cohort([GOOD_DONOR], registered=False)], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_underage_donor_is_deferred():
    donor = {"age": 16, "weight_kg": 70, "hb": 14.0}
    result = process_donor_cohort([make_cohort([donor])], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_underweight_donor_is_deferred():
    donor = {"age": 30, "weight_kg": 49, "hb": 14.0}
    result = process_donor_cohort([make_cohort([donor])], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_low_hemoglobin_standard_cohort_keeps_processing():
    low_hb = {"age": 30, "weight_kg": 70, "hb": 11.0}
    result = process_donor_cohort([make_cohort([low_hb, GOOD_DONOR])], VOLUME)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hemoglobin_high_altitude_resets_total_and_stops_cohort():
    low_hb = {"age": 30, "weight_kg": 70, "hb": 11.0}
    cohort = make_cohort([GOOD_DONOR, low_hb, GOOD_DONOR], cohort_type="high_altitude")
    result = process_donor_cohort([cohort], VOLUME)
    # the 450 ml already collected is wiped and the last donor is never seen
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_hemoglobin_donor_is_deferred():
    high_hb = {"age": 30, "weight_kg": 70, "hb": 19.0}
    result = process_donor_cohort([make_cohort([high_hb])], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_fast_track_bonus_added():
    result = process_donor_cohort([make_cohort([GOOD_DONOR], fast_track=True)], VOLUME)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_high_deferral_status():
    bad = {"age": 10, "weight_kg": 70, "hb": 14.0}
    result = process_donor_cohort([make_cohort([bad] * 5 + [GOOD_DONOR])], VOLUME)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


# ---------------------------------------------------------------------------
# verify_storage_centrifuge
# ---------------------------------------------------------------------------
def test_centrifuge_no_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_stable():
    assert verify_storage_centrifuge([[3500, 3600, 3550]]) == "STABLE"


def test_centrifuge_abort_on_two_consecutive_drops():
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"
