import pytest  # pylint: disable=unused-import

import pandas as pd
from datetime import timedelta
from visuals.shared import fix_timedelta_plot


def test_fix_timedelta_plot():
    timedelta_df0 = timedelta(0)
    timedelta_df1 = pd.Timedelta("00:31:31")
    active_date = "2020/1/1"
    dflt_active_date = "1970/1/1"

    # cases where both timedelta and active date are povided
    assert fix_timedelta_plot(timedelta_df0, active_date) == (
        timedelta_df0 + pd.to_datetime(active_date)
    )
    assert fix_timedelta_plot(timedelta_df1, active_date) == (
        timedelta_df1 + pd.to_datetime(active_date)
    )

    # cases where timedelta is provided but active date is not
    assert fix_timedelta_plot(timedelta_df0,) == (
        timedelta_df0 + pd.to_datetime(dflt_active_date)
    )
    assert fix_timedelta_plot(timedelta_df1,) == (
        timedelta_df1 + pd.to_datetime(dflt_active_date)
    )
