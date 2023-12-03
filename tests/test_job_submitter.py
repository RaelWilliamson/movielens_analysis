from unittest.mock import patch
from dependencies.job_submitter import execute_pyspark_script


@patch("subprocess.run")
def test_execute_pyspark_script_local(mock_subprocess_run):
    script_name = "test_script.py"
    config_path = "config.yaml"
    env = "local"

    execute_pyspark_script(script_name, config_path, env)

    mock_subprocess_run.assert_called_once_with(
        f"spark-submit --master local[*] {script_name} {config_path}", shell=True
    )


@patch("subprocess.run")
def test_execute_pyspark_script_cluster(mock_subprocess_run):
    script_name = "test_script.py"
    config_path = "config.yaml"
    env = "cluster"

    execute_pyspark_script(script_name, config_path, env)

    mock_subprocess_run.assert_called_once_with(
        f"spark-submit --master spark://spark-master:7077 --deploy-mode client {script_name} {config_path}",
        shell=True,
    )
