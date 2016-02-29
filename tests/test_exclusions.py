from datetime import datetime
from recurrence import Recurrence, Rule
import recurrence


def test_exclusion_date():
    rule = Rule(
        recurrence.DAILY
    )

    pattern = Recurrence(
        dtstart=datetime(2014, 1, 2, 0, 0, 0),
        dtend=datetime(2014, 1, 4, 0, 0, 0),
        rrules=[rule],
        exdates=[
            datetime(2014, 1, 3, 0, 0, 0)
        ]
    )

    occurrences = [
        instance for instance in
        pattern.occurrences()
    ]

    assert occurrences == [
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 4, 0, 0, 0),
    ]

    assert 2 == pattern.count()


def test_exclusion_date_no_limits():
    pattern = Recurrence(
        rdates=[
            datetime(2014, 1, 1, 0, 0, 0),
            datetime(2014, 1, 2, 0, 0, 0),
        ],
        exdates=[
            datetime(2014, 1, 2, 0, 0, 0)
        ]
    )

    occurrences = [
        instance for instance in
        pattern.occurrences()
    ]

    assert occurrences == [
        datetime(2014, 1, 1, 0, 0, 0),
    ]

    assert 1 == pattern.count()


def test_exclusion_rule():
    inclusion_rule = Rule(
        recurrence.DAILY
    )

    exclusion_rule = Rule(
        recurrence.WEEKLY,
        byday=recurrence.THURSDAY
    )

    pattern = Recurrence(
        dtstart=datetime(2014, 1, 2, 0, 0, 0),
        dtend=datetime(2014, 1, 4, 0, 0, 0),
        rrules=[inclusion_rule],
        exrules=[exclusion_rule]
    )

    occurrences = [
        instance for instance in
        pattern.occurrences()
    ]

    assert occurrences == [
        datetime(2014, 1, 3, 0, 0, 0),
        datetime(2014, 1, 4, 0, 0, 0),
    ]

    assert 2 == pattern.count()


def test_exclusion_rule_feb29():
    inclusion_rule = Rule(
        recurrence.DAILY
    )

    pattern = Recurrence(
        dtstart=datetime(2016, 1, 1, 0, 0, 0),
        dtend=datetime(2017, 1, 1, 0, 0, 0),
        rrules=[inclusion_rule],
        exdates = [datetime(2016, 2, 29, 0, 0),]
    )

    # This works correctly
    assert pattern.between(datetime(2016, 2, 29, 0, 0), datetime(2016, 2, 29, 23, 59)) == []

    pattern = Recurrence(
        rrules=[inclusion_rule],
        exdates = [datetime(2016, 2, 29, 0, 0),]
    )

    # Without dtstart/dtend this doesn't work: I would expect
    # Feb 29th to be excluded just as the previous assert
    assert pattern.between(datetime(2016, 2, 29, 0, 0), datetime(2016, 2, 29, 23, 59)) == []
