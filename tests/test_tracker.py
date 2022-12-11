import json
import pytest

from typer.testing import CliRunner

import application_tracker.tracker
from application_tracker import cli, __app_name__, __version__, SUCCESS, DB_READ_ERROR, tracker

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    application = [{"Title": "Data Scientist",
                    "Description": "We are looking for scientists who are passionate..."}]
    db_file = tmp_path / "tracker.json"
    with db_file.open('w') as db:
        json.dump(application, db, indent=4)
    return db_file


# Now create some test data with different test cases along with the expected result
test_data1 = {
    "title": "Data Scientist",
    "description": ["We are looking for scientists..."],
    "application": {
        "title": "Data Scientist",
        "description": "We are looking for scientists..."
    }
}
test_data2 = {
    "title": "Junior Data Scientist",
    "description": ["We", "are", "looking", "for", "scientists..."],
    "application": {
        "title": "Junior Data Scientist",
        "description": "We are looking for scientists..."
    }
}


@pytest.mark.parametrize(
    "title, description, expected",
    [pytest.param(
        test_data1["title"],
        test_data1["description"],
        (test_data1["application"], SUCCESS)
    ),
        pytest.param(
            test_data2["title"],
            test_data2["description"],
            (test_data2["application"], SUCCESS)
        )]

)
def test_add(mock_json_file, title, description, expected):
    applier = tracker.Applier(mock_json_file)
    assert applier.add(title, description) == expected
    read = applier._db_handler.read_applications()
    assert len(read.application_list) == 2

