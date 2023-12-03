import subprocess
import typer

app = typer.Typer()


def execute_pyspark_script(script_name: str, config_path: str, env: str):
    """
    Executes a PySpark script either locally or on a cluster based on the environment.

    Args:
    - script_name (str): Name of the PySpark script to execute.
    - config_path (str): Path to the configuration file.
    - env (str): Environment flag, "local" or "cluster".
    """
    if env == "cluster":
        typer.echo("Submitting job to cluster")
        # Formulate the command to submit job to a Spark cluster
        command = f"spark-submit --master spark://spark-master:7077 --deploy-mode client {script_name} {config_path}"
    else:
        typer.echo("Running job locally")
        # Formulate the command to run job locally
        command = f"spark-submit --master local[*] {script_name} {config_path}"

    # Run the Spark job
    subprocess.run(command, shell=True)


@app.command()
def main(
    env: str = typer.Argument(...),
    config: str = typer.Argument(...),
    script: str = typer.Argument(...),
):
    """
    Main function to execute the PySpark job based on provided arguments.

    Args:
    - env (str): Environment flag, "local" or "cluster".
    - config (str): Path to the configuration file.
    - script (str): Name of the PySpark script to execute.
    """
    execute_pyspark_script(script, config, env)


if __name__ == "__main__":
    app()
