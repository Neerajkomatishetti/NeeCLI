from click.testing import CliRunner
from cli import cli

def test_help_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
