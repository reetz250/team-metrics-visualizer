import pytest
import plotly.graph_objects as go

from database import db
from test.mock_objects import UserMock

from structure.measurements import OTMeasurement
from structure.organization import Team

from visuals import OvertimeChartController
from datetime import date, timedelta


@pytest.mark.usefixtures("app")
class TestOvertimeVisual:
    @pytest.fixture(scope="module")
    # Create some OT measurements
    def dates(self):
        dates = (
            {date(2019, 3, 10), date(2019, 5, 5), date(2019, 5, 10)}
            | {date(2019, 8, day) for day in range(1, 32)}
            | {date(2019, 9, day) for day in range(1, 10)}
            | {date(2019, 10, 28)}
        )
        return dates

    def team(self):
        team = Team(parent_team=None, code="ABC", name="Team ABC")
        return team

    def set_db(self, dates, team):
        for measurement_date in dates:
            db.session.add(
                OTMeasurement(
                    measurement_date=measurement_date,
                    team=team,
                    workdays_fix=20,
                    workdays_actual=20,
                    overtime=timedelta(hours=10, minutes=15),
                )
            )
        db.session.commit()

    def mocker(self, mocker):
        return mocker.patch("visuals.work_time.current_user", UserMock())

    @pytest.fixture(scope="function")
    def ot_visual(self):
        visual = OvertimeChartController()
        return visual

    def test_visual_initialized(self, ot_visual: OvertimeChartController):
        assert ot_visual is not None

    def test_earliest_and_latest_date(self, ot_visual, mocker, dates, team):

        self.set_db(dates, team)
        self.mocker(mocker)

        # Check if dates in overtime chart match
        assert ot_visual.get_earliest_date() == min(dates)
        assert ot_visual.get_latest_date() == max(dates)

    def test_added_traces_in_update(self, ot_visual, mocker, dates, team):

        self.set_db(dates, team)
        self.mocker(mocker)

        data, layout = ot_visual.update(
            ot_visual.get_latest_date(), ot_visual.get_latest_date()
        )

        first_trace = go.Box(
            x=["2019-10-01 00:00:00"],
            name="",
            marker_color="rgba(0, 0, 0, 0)",
            hoverinfo="none",
        )

        last_trace = go.Box(
            x=["2019-10-01 00:00:00"],
            name=" ",
            marker_color="rgba(0, 0, 0, 0)",
            hoverinfo="none",
        )

        assert layout is not None
        assert first_trace in data
        assert last_trace in data
