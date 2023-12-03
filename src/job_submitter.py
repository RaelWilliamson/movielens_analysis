import argparse
import subprocess


def execute_pyspark_script(script_name, config_path, env):
    if env == "cluster":
        print("Submitting job to cluster")
        command = f"spark-submit --master spark://spark-master:7077 --deploy-mode client {script_name} {config_path}"
        subprocess.run(command, shell=True)
    else:
        print("Running job locally")
        command = f"spark-submit --master local[*] {script_name} {config_path}"
        subprocess.run(command, shell=True)


def main(env, config, script):
    execute_pyspark_script(script, config, env)

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job_Submitter")
    parser.add_argument("--env", required=False, default="local")
    parser.add_argument("--config", required=True)
    parser.add_argument("--script", required=True)
    args = vars(parser.parse_args())
    main(args["env"], args["config"], args["script"])
