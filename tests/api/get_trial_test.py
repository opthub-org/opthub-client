"""Test for retrieving match trial information."""

import tests.api._common as common
from opthub_client.api import MatchTrialStatus, OptHub

EXPECTED_OBJECTIVE = 10.0
EXPECTED_SCORE = 10.0


def test_get_trial() -> None:
    """Test for retrieving match trial information."""
    with OptHub(common.TEST_API_KEY) as api:
        trial = api.match(common.TEST_MATCH).get_trial(2)
        assert trial.status.type == MatchTrialStatus.SUCCESS  # noqa: S101
        assert trial.wait_evaluation().objective.scalar == EXPECTED_OBJECTIVE  # noqa: S101
        assert trial.wait_scoring().value == EXPECTED_SCORE  # noqa: S101
