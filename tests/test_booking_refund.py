import pytest

from src.booking_refund import is_refundable

# Requirement 3.2: a refund is allowed only when flexible_rate is True
# and the cancellation is at least 48 hours before check in.


@pytest.mark.parametrize(
    "hours_before_checkin, flexible_rate, expected",
    [
        (48, True, True),  # exactly 48 hours is refundable
        (49, True, True),
        (72, True, True),
        (500, True, True),
        (47, True, False),  # just under 48 hours
        (24, True, False),
        (1, True, False),
        (0, True, False),
        (0, False, False),  # non-flexible rate is never refundable
        (47, False, False),
        (48, False, False),
        (49, False, False),
        (500, False, False),
    ],
)
def test_refund_decision_follows_rate_and_cancellation_time(
    hours_before_checkin, flexible_rate, expected
):
    # Arrange: inputs and expected result come from the parameters
    # Act
    result = is_refundable(hours_before_checkin, flexible_rate)
    # Assert
    assert result is expected


@pytest.mark.parametrize("flexible_rate", [True, False])
def test_negative_hours_raises_value_error(flexible_rate):
    # Arrange
    hours_before_checkin = -1
    # Act and Assert
    with pytest.raises(ValueError):
        is_refundable(hours_before_checkin, flexible_rate)


@pytest.mark.parametrize(
    "hours_before_checkin, flexible_rate",
    [
        ("48", True),  # hours is a string
        (48.0, True),  # hours is a float
        (None, True),  # hours is None
        (True, True),  # hours is a bool, not a valid integer
        (48, 1),  # flexible_rate is an int, not a bool
        (48, 0),  # flexible_rate is an int, not a bool
        (48, "True"),  # flexible_rate is a string
        (48, None),  # flexible_rate is None
    ],
)
def test_invalid_argument_type_raises_type_error(hours_before_checkin, flexible_rate):
    # Arrange: invalid types come from the parameters
    # Act and Assert
    with pytest.raises(TypeError):
        is_refundable(hours_before_checkin, flexible_rate)
