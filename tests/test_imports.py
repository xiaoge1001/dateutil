import sys
import unittest
import pytest

MODULE_TYPE = type(sys)


# Tests live in datetutil/test which cause a RuntimeWarning for Python2 builds.
# But since we expect lazy imports tests to fail for Python < 3.7  we'll ignore those
# warnings with this filter.

def filter_import_warning(f):
    return f


@pytest.fixture(scope="function")
def clean_import():
    """Create a somewhat clean import base for lazy import tests"""
    du_modules = {
        mod_name: mod
        for mod_name, mod in sys.modules.items()
        if mod_name.startswith("dateutil")
    }

    other_modules = {
        mod_name for mod_name in sys.modules if mod_name not in du_modules
    }

    for mod_name in du_modules:
        del sys.modules[mod_name]

    yield

    # Delete anything that wasn't in the origin sys.modules list
    for mod_name in list(sys.modules):
        if mod_name not in other_modules:
            del sys.modules[mod_name]

    # Restore original modules
    for mod_name, mod in du_modules.items():
        sys.modules[mod_name] = mod


@filter_import_warning
@pytest.mark.parametrize(
    "module",
    ["easter", "parser", "relativedelta", "rrule", "tz", "utils", "zoneinfo"],
)
def test_lazy_import(clean_import, module):
    """Test that dateutil.[submodule] works for py version > 3.7"""

    import dateutil, importlib

    if sys.version_info < (3, 7):
        pytest.xfail("Lazy loading does not work for Python < 3.7")

    mod_obj = getattr(dateutil, module, None)
    assert isinstance(mod_obj, MODULE_TYPE)

    mod_imported = importlib.import_module("dateutil.%s" % module)
    assert mod_obj is mod_imported


HOST_IS_WINDOWS = sys.platform.startswith('win')


def test_import_version_str():
    """ Test that dateutil.__version__ can be imported"""
    from dateutil import __version__


def test_import_version_root():
    import dateutil
    assert hasattr(dateutil, '__version__')


# Test that dateutil.easter-related imports work properly
def test_import_easter_direct():
    import dateutil.easter


def test_import_easter_from():
    from dateutil import easter


def test_import_easter_start():
    from dateutil.easter import easter


#  Test that dateutil.parser-related imports work properly
def test_import_parser_direct():
    import dateutil.parser


def test_import_parser_from():
    from dateutil import parser


def test_import_parser_all():
    # All interface
    from dateutil.parser import parse
    from dateutil.parser import parserinfo

    # Other public classes
    from dateutil.parser import parser

    for var in (parse, parserinfo, parser):
        assert var is not None


# Test that dateutil.relativedelta-related imports work properly
def test_import_relative_delta_direct():
    import dateutil.relativedelta


def test_import_relative_delta_from():
    from dateutil import relativedelta

def test_import_relative_delta_all():
    from dateutil.relativedelta import relativedelta
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

    for var in (relativedelta, MO, TU, WE, TH, FR, SA, SU):
        assert var is not None

    # In the public interface but not in all
    from dateutil.relativedelta import weekday
    assert weekday is not  None


# Test that dateutil.rrule related imports work properly
def test_import_rrule_direct():
    import dateutil.rrule


def test_import_rrule_from():
    from dateutil import rrule


def test_import_rrule_all():
    from dateutil.rrule import rrule
    from dateutil.rrule import rruleset
    from dateutil.rrule import rrulestr
    from dateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY
    from dateutil.rrule import HOURLY, MINUTELY, SECONDLY
    from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU

    rr_all = (rrule, rruleset, rrulestr,
              YEARLY, MONTHLY, WEEKLY, DAILY,
              HOURLY, MINUTELY, SECONDLY,
              MO, TU, WE, TH, FR, SA, SU)

    for var in rr_all:
       assert var is not None

    # In the public interface but not in all
    from dateutil.rrule import weekday
    assert weekday is not None


# Test that dateutil.tz related imports work properly
def test_import_tztest_direct():
    import dateutil.tz


def test_import_tz_from():
    from dateutil import tz


def test_import_tz_all():
    from dateutil.tz import tzutc
    from dateutil.tz import tzoffset
    from dateutil.tz import tzlocal
    from dateutil.tz import tzfile
    from dateutil.tz import tzrange
    from dateutil.tz import tzstr
    from dateutil.tz import tzical
    from dateutil.tz import gettz
    from dateutil.tz import tzwin
    from dateutil.tz import tzwinlocal
    from dateutil.tz import UTC
    from dateutil.tz import datetime_ambiguous
    from dateutil.tz import datetime_exists
    from dateutil.tz import resolve_imaginary

    tz_all = ["tzutc", "tzoffset", "tzlocal", "tzfile", "tzrange",
              "tzstr", "tzical", "gettz", "datetime_ambiguous",
              "datetime_exists", "resolve_imaginary", "UTC"]

    tz_all += ["tzwin", "tzwinlocal"] if sys.platform.startswith("win") else []
    lvars = locals()

    for var in tz_all:
        assert lvars[var] is not None

# Test that dateutil.tzwin related imports work properly
@pytest.mark.skipif(not HOST_IS_WINDOWS, reason="Requires Windows")
def test_import_tz_windows_direct():
    import dateutil.tzwin


@pytest.mark.skipif(not HOST_IS_WINDOWS, reason="Requires Windows")
def test_import_tz_windows_from():
    from dateutil import tzwin


@pytest.mark.skipif(not HOST_IS_WINDOWS, reason="Requires Windows")
def test_import_tz_windows_star():
    from dateutil.tzwin import tzwin
    from dateutil.tzwin import tzwinlocal

    tzwin_all = [tzwin, tzwinlocal]

    for var in tzwin_all:
        assert var is not None


# Test imports of Zone Info
def test_import_zone_info_direct():
    import dateutil.zoneinfo


def test_import_zone_info_from():
    from dateutil import zoneinfo


def test_import_zone_info_star():
    from dateutil.zoneinfo import gettz
    from dateutil.zoneinfo import gettz_db_metadata
    from dateutil.zoneinfo import rebuild

    zi_all = (gettz, gettz_db_metadata, rebuild)

    for var in zi_all:
        assert var is not None
