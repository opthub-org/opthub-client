"""Solution submission test for Public REST API wrapper."""

import tests.api._common as common
from opthub_client.api import OptHub

EXPECTED_SCORE = 4.4


def test_submit() -> None:
    """Test for submission of the solution."""
    with OptHub(common.TEST_API_KEY) as api:
        match = api.match(common.TEST_MATCH)
        submit = match.submit([1.1, -2.2, 3.3])
        score = submit.wait_scoring(timeout=5)
        assert score == EXPECTED_SCORE  # noqa: S101
