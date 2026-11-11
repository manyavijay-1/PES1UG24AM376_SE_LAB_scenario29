"""
Lab 6 - Part 2: BRANCH coverage tests for blood_donation_screening.py

Every decision in the module is exercised for BOTH its True and False outcome,
including the individual operands of compound conditions (e.g. `age < 17`
vs `weight < 50`) and the exact boundary values (17, 50, 12.5, 18.0, 3000).

Run (from the "Lab 6" folder):
    coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening.py
    coverage report -m
"""

import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge

VOLUME = 450


def make_cohort(donors, registered=True, cohort_type="standard", fast_track=False):
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


def donor(age=25, weight_kg=65, hb=14.0):
    return {"age": age, "weight_kg": weight_kg, "hb": hb}


# ===========================================================================
# process_donor_cohort
# ===========================================================================

# --- Decision: `not isinstance(cohorts, list) or standard_volume_ml <= 0` ---
@pytest.mark.parametrize("bad_cohorts", ["text", None, {"a": 1}, (1, 2)])
def test_cohorts_not_a_list_raises(bad_cohorts):          # first operand True
    with pytest.raises(ValueError):
        process_donor_cohort(bad_cohorts, VOLUME)


@pytest.mark.parametrize("bad_volume", [0, -1, -450])
def test_non_positive_volume_raises(bad_volume):          # second operand True
    with pytest.raises(ValueError):
        process_donor_cohort([make_cohort([donor()])], bad_volume)


def test_valid_inputs_do_not_raise():                     # both operands False
    assert process_donor_cohort([make_cohort([donor()])], 1)["collected_ml"] == 1


# --- Loop: `for cohort in cohorts` (zero iterations / many iterations) -----
def test_empty_cohort_list_is_zero_yield():
    assert process_donor_cohort([], VOLUME) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_multiple_cohorts_are_summed():
    cohorts = [make_cohort([donor()]), make_cohort([donor(), donor()])]
    assert process_donor_cohort(cohorts, VOLUME) == {"collected_ml": 1350, "status": "ACCEPTED"}


# --- Decision: `if not cohort.get("clinic_registered", False)` --------------
def test_unregistered_cohort_skipped():                   # True  -> continue
    result = process_donor_cohort([make_cohort([donor()], registered=False)], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_missing_registration_key_defaults_to_skipped():  # .get default False
    result = process_donor_cohort([{"donors": [donor()]}], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_registered_cohort_processed():                   # False -> continue not taken
    result = process_donor_cohort([make_cohort([donor()])], VOLUME)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_unregistered_cohort_does_not_block_later_cohorts():
    cohorts = [make_cohort([donor()], registered=False), make_cohort([donor()])]
    assert process_donor_cohort(cohorts, VOLUME)["collected_ml"] == 450


# --- Loop: `for donor in donors` (zero iterations) + .get defaults ---------
def test_registered_cohort_without_donors_key():
    result = process_donor_cohort([{"clinic_registered": True}], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_registered_cohort_with_empty_donor_list():
    result = process_donor_cohort([make_cohort([])], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_missing_cohort_type_defaults_to_standard():
    cohort = {"clinic_registered": True, "donors": [donor(hb=10.0), donor()]}
    # standard behaviour: low-Hb donor deferred, loop continues, next donor accepted
    assert process_donor_cohort([cohort], VOLUME) == {"collected_ml": 450, "status": "ACCEPTED"}


def test_empty_donor_dict_uses_defaults_and_is_deferred():
    # age defaults to 0 -> `age < 17` True
    assert process_donor_cohort([make_cohort([{}])], VOLUME) == {
        "collected_ml": 0,
        "status": "ZERO_YIELD",
    }


# --- Decision: `age < 17 or weight < 50` (each operand, both sides) --------
def test_age_16_deferred():                               # age True
    assert process_donor_cohort([make_cohort([donor(age=16)])], VOLUME)["collected_ml"] == 0


def test_age_17_boundary_accepted():                      # age False (boundary)
    assert process_donor_cohort([make_cohort([donor(age=17)])], VOLUME)["collected_ml"] == 450


def test_weight_49_deferred():                            # weight True
    assert process_donor_cohort([make_cohort([donor(weight_kg=49)])], VOLUME)["collected_ml"] == 0


def test_weight_50_boundary_accepted():                   # weight False (boundary)
    assert process_donor_cohort([make_cohort([donor(weight_kg=50)])], VOLUME)["collected_ml"] == 450


def test_age_and_weight_both_fail():
    assert process_donor_cohort([make_cohort([donor(age=10, weight_kg=30)])], VOLUME)["collected_ml"] == 0


def test_demographic_deferral_does_not_stop_cohort():     # `continue`, not `break`
    cohort = make_cohort([donor(age=10), donor()], cohort_type="high_altitude")
    assert process_donor_cohort([cohort], VOLUME)["collected_ml"] == 450


# --- Decision chain: hb < 12.5 / hb > 18.0 / else --------------------------
def test_hb_12_4_deferred_standard():                     # hb < 12.5 True, type != high_altitude
    result = process_donor_cohort([make_cohort([donor(hb=12.4)])], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_hb_12_5_boundary_accepted():                     # hb < 12.5 False, > 18 False -> else
    assert process_donor_cohort([make_cohort([donor(hb=12.5)])], VOLUME)["collected_ml"] == 450


def test_hb_18_0_boundary_accepted():                     # hb > 18.0 False (boundary) -> else
    assert process_donor_cohort([make_cohort([donor(hb=18.0)])], VOLUME)["collected_ml"] == 450


def test_hb_18_1_deferred():                              # hb > 18.0 True
    result = process_donor_cohort([make_cohort([donor(hb=18.1)])], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_missing_hb_defaults_to_zero_and_is_deferred():
    d = {"age": 30, "weight_kg": 70}
    assert process_donor_cohort([make_cohort([d])], VOLUME)["collected_ml"] == 0


def test_low_hb_standard_cohort_continues_to_next_donor():
    cohort = make_cohort([donor(hb=10.0), donor()])
    assert process_donor_cohort([cohort], VOLUME) == {"collected_ml": 450, "status": "ACCEPTED"}


# --- Decision: `cohort_type == "high_altitude"` (inside hb < 12.5) ---------
def test_low_hb_high_altitude_wipes_total_and_breaks():   # True -> reset + break
    cohort = make_cohort([donor(), donor(), donor(hb=10.0), donor()], cohort_type="high_altitude")
    assert process_donor_cohort([cohort], VOLUME) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_with_normal_hb_is_not_affected():  # False for high_altitude + ok hb
    cohort = make_cohort([donor(), donor()], cohort_type="high_altitude")
    assert process_donor_cohort([cohort], VOLUME)["collected_ml"] == 900


def test_high_altitude_reset_also_wipes_earlier_cohorts():
    cohorts = [
        make_cohort([donor()]),                                           # +450
        make_cohort([donor(hb=10.0)], cohort_type="high_altitude"),       # reset to 0
    ]
    assert process_donor_cohort(cohorts, VOLUME) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_break_only_stops_its_own_cohort():
    cohorts = [
        make_cohort([donor(hb=10.0)], cohort_type="high_altitude"),
        make_cohort([donor()]),                                           # still processed
    ]
    assert process_donor_cohort(cohorts, VOLUME) == {"collected_ml": 450, "status": "ACCEPTED"}


# --- Decision: `cohort.get("fast_track", False)` ---------------------------
def test_fast_track_true_adds_bonus():
    result = process_donor_cohort([make_cohort([donor()], fast_track=True)], VOLUME)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_false_no_bonus():
    result = process_donor_cohort([make_cohort([donor()], fast_track=False)], VOLUME)
    assert result["collected_ml"] == 450


def test_fast_track_missing_key_no_bonus():
    cohort = {"clinic_registered": True, "donors": [donor()]}
    assert process_donor_cohort([cohort], VOLUME)["collected_ml"] == 450


def test_fast_track_bonus_applies_even_after_high_altitude_break():
    # break only leaves the donor loop, so the +50 bonus still runs afterwards
    cohort = make_cohort([donor(hb=10.0)], cohort_type="high_altitude", fast_track=True)
    assert process_donor_cohort([cohort], VOLUME) == {"collected_ml": 50, "status": "ACCEPTED"}


def test_fast_track_on_cohort_with_no_donors_still_adds_bonus():
    result = process_donor_cohort([make_cohort([], fast_track=True)], VOLUME)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_fast_track_not_applied_to_unregistered_cohort():
    result = process_donor_cohort([make_cohort([donor()], registered=False, fast_track=True)], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# --- Decision: `deferred_count > 4` ----------------------------------------
def test_five_deferrals_is_high_deferral():               # True
    donors = [donor(age=10)] * 5
    assert process_donor_cohort([make_cohort(donors)], VOLUME) == {
        "collected_ml": 0,
        "status": "HIGH_DEFERRAL",
    }


def test_high_deferral_takes_priority_over_collected_volume():
    donors = [donor(age=10)] * 5 + [donor()]
    assert process_donor_cohort([make_cohort(donors)], VOLUME) == {
        "collected_ml": 450,
        "status": "HIGH_DEFERRAL",
    }


def test_four_deferrals_boundary_is_not_high_deferral():  # False (boundary)
    donors = [donor(age=10)] * 4 + [donor()]
    assert process_donor_cohort([make_cohort(donors)], VOLUME) == {
        "collected_ml": 450,
        "status": "ACCEPTED",
    }


def test_deferrals_accumulate_across_cohorts():
    cohorts = [make_cohort([donor(age=10)] * 3), make_cohort([donor(hb=19.0)] * 2)]
    assert process_donor_cohort(cohorts, VOLUME)["status"] == "HIGH_DEFERRAL"


# --- Decision: `total_collected_ml == 0` -----------------------------------
def test_zero_total_with_few_deferrals_is_zero_yield():   # True
    assert process_donor_cohort([make_cohort([donor(age=10)])], VOLUME) == {
        "collected_ml": 0,
        "status": "ZERO_YIELD",
    }


def test_nonzero_total_is_accepted():                     # False
    assert process_donor_cohort([make_cohort([donor()])], VOLUME) == {
        "collected_ml": 450,
        "status": "ACCEPTED",
    }


# ===========================================================================
# verify_storage_centrifuge
# ===========================================================================

# --- Decision: `if not centrifuge_runs` ------------------------------------
@pytest.mark.parametrize("empty", [[], None])
def test_centrifuge_no_data(empty):                       # True
    assert verify_storage_centrifuge(empty) == "NO_DATA"


# --- Loops: runs / readings (zero and many iterations) ---------------------
def test_centrifuge_run_with_no_readings_is_stable():
    assert verify_storage_centrifuge([[]]) == "STABLE"


def test_centrifuge_all_runs_stable():
    assert verify_storage_centrifuge([[3500, 3600], [3200, 4000]]) == "STABLE"


# --- Decision: `rpm < 3000` ------------------------------------------------
def test_rpm_exactly_3000_is_not_a_drop():                # False (boundary)
    assert verify_storage_centrifuge([[3000, 3000, 3000]]) == "STABLE"


def test_rpm_2999_is_a_drop():                            # True (boundary)
    assert verify_storage_centrifuge([[2999, 2999]]) == "ABORT_SPIN"


# --- Decision: `rpm_drop_streak >= 2` --------------------------------------
def test_single_drop_does_not_abort():                    # streak == 1 -> False
    assert verify_storage_centrifuge([[3500, 2900, 3500]]) == "STABLE"


def test_single_drop_at_end_of_run_does_not_abort():
    assert verify_storage_centrifuge([[3500, 2900]]) == "STABLE"


def test_two_consecutive_drops_abort():                   # streak == 2 -> True
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_long_streak_aborts_at_second_reading():
    assert verify_storage_centrifuge([[100, 100, 100, 100]]) == "ABORT_SPIN"


# --- else branch: streak reset ---------------------------------------------
def test_recovery_resets_streak():
    assert verify_storage_centrifuge([[2900, 3500, 2900, 3500, 2900]]) == "STABLE"


def test_streak_resets_between_runs():
    # one drop at the end of run 1 + one at the start of run 2 must NOT abort
    assert verify_storage_centrifuge([[3500, 2900], [2900, 3500]]) == "STABLE"


def test_abort_found_in_later_run():
    assert verify_storage_centrifuge([[3500, 3600], [2000, 1900]]) == "ABORT_SPIN"


def test_abort_in_first_run_short_circuits_remaining_runs():
    assert verify_storage_centrifuge([[2000, 2000], [3500]]) == "ABORT_SPIN"
