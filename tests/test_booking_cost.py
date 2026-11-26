import pytest

from src.booking_cost import calculate_booking_cost

# Requirement 3.1: total charge = nights x nightly_rate_cents.
# Every booked night is charged. No free nights or long stay discount applies.


@pytest.mark.parametrize(
    "nights, nightly_rate_cents, expected",
    [
        (1, 15000, 15000),  # lower boundary of nights
        (2, 15000, 30000),
        (6, 15000, 90000),  # just below 7 nights
        (7, 15000, 105000),  # 7 nights: every night must be charged
        (8, 15000, 120000),
        (29, 15000, 435000),
        (30, 15000, 450000),  # upper boundary of nights
        (1, 0, 0),  # zero rate gives zero charge
        (6, 0, 0),
        (7, 0, 0),
        (30, 0, 0),
    ],
)
def test_valid_stay_returns_nights_times_rate_as_int(nights, nightly_rate_cents, expected):
    # Arrange: nights, nightly_rate_cents and expected come from the parameters
    # Act jajaj
    result = calculate_booking_cost(nights, nightly_rate_cents)
    # Assert
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize(
    "nights, nightly_rate_cents",
    [
        (0, 15000),  # below minimum nights
        (-1, 15000),  # negative nights
        (31, 15000),  # above maximum nights
        (1, -1),  # negative nightly rate
        (30, -100),  # negative nightly rate
    ],
)
def test_out_of_range_argument_raises_value_error(nights, nightly_rate_cents):
    # Arrange: invalid values come from the parameters
    # Act and Assert
    with pytest.raises(ValueError):
        calculate_booking_cost(nights, nightly_rate_cents)


@pytest.mark.parametrize(
    "nights, nightly_rate_cents",
    [
        ("3", 15000),  # nights is a string
        (3.0, 15000),  # nights is a float
        (None, 15000),  # nights is None
        (True, 15000),  # nights is a bool, not a valid integer
        (3, "15000"),  # rate is a string
        (3, 150.5),  # rate is a float
        (3, None),  # rate is None
        (3, True),  # rate is a bool, not a valid integer
    ],
)
def test_invalid_argument_type_raises_type_error(nights, nightly_rate_cents):
    # Arrange: invalid types come from the parameters
    # Act and Assert
    with pytest.raises(TypeError):
        calculate_booking_cost(nights, nightly_rate_cents)
