import json
import pytest

from typer.testing import CliRunner
from src import cli, __app_name__, __version__, SUCCESS, DB_READ_ERROR, tracker

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    application = [{"Title": "Data Scientist",
                    "Company": "Oracle",
                    "Description": "We are looking for scientists who are passionate about data and are eager to tackle big challenges using Data Science and Machine Learning. The main focus of this role is to solve non-trivial business problems in Fortune 500 companies. This person will mostly work with a mix of structured and unstructured and use scientific methods and state-of-the-art techniques and tools to help our customers achieve their business objectives.",
                    "Location": "London",
                    "Remote": True,
                    "Close Date": "25/12/2022",
                    "Date Applied": "10/12/2022"}]
    db_file = tmp_path / "tracker.json"
    with db_file.open('w') as db:
        json.dump(application, db, indent=4)
    return db_file


# Now create some test data with different test cases along with the expected result
test_data1 = {
    "Title": ["Data", "Scientist"],
    "Description": "We are looking for scientists...",
    "Remote": True,
    "application": {
        "Title": "Data Scientist",
        "Description": "We are looking for scientists...",
        "Remote": True
    }
}
test_data2 = {
    "Title": ["Junior Data Scientist"],
    "Description": "We are looking for scientists...",
    "Remote": False,
    "application": {
        "Title": "Junior Data Scientist",
        "Description": "We are looking for scientists...",
        "Remote": False
    }
}
