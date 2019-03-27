import click
import logging, coloredlogs
from conu import DockerRunBuilder, DockerBackend
from termcolor import colored

import os

coloredlogs.install(level='DEBUG')



#python3 main.py --image quay.io/jkremser/openshift-spark --tag 2.4.0

# image = 'quay.io/jkremser/openshift-spark'
# tag = '2.4.0'
# backend = DockerBackend(logging_level=logging.DEBUG)

@click.command()
@click.option('--image', '-i', prompt='container image', help='Container image with Spark.')
@click.option('--tag', '-t', prompt='tag', default='latest', help='Specific tag of the image.')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output.')
def check(image, tag, verbose):
    """Simple verification tool that check the compatibility with Spark Operator"""
    logging_level = logging.DEBUG if verbose else logging.ERROR
    logging.getLogger("urllib3").setLevel(logging_level)
    logging.getLogger("docker").setLevel(logging_level)

    with DockerBackend(logging_level=logging_level) as backend:
        results = {}

        # the image will be pulled if it's not present
        i = backend.ImageClass(image, tag=tag)

        # the command to run in a container
        run_params = DockerRunBuilder(additional_opts=['--entrypoint', ''], command=['sleep', '3600'])
        container = i.run_via_binary(run_params)

        assert container.is_running(), "Container must be running"
        try:
            # we can also access it directly on disk and compare
            with container.mount() as fs:
                if os.path.lexists(fs.p('/opt/spark')):
                    resolved_spark_home = os.readlink(fs.p('/opt/spark'))
                else:
                    resolved_spark_home = '/opt/spark'

                launch_script_is_present = fs.file_is_present('/launch.sh') or fs.file_is_present(resolved_spark_home + '/bin/launch.sh')
                results["launch_script_is_present"] = {"result": launch_script_is_present, "message": "File /launch.sh should be present on the image"}

                if launch_script_is_present:
                    launch_script = fs.read_file('/launch.sh') if fs.file_is_present('/launch.sh') else fs.read_file(resolved_spark_home + '/bin/launch.sh')
                    metrics_support = 'SPARK_METRICS_ON' in launch_script
                    master_address_support = 'SPARK_MASTER_ADDRESS' in launch_script
                else:
                    metrics_support = master_address_support = False

                results["metrics_support"] = {"result": metrics_support, "message": "File /launch.sh does contain SPARK_METRICS_ON"}
                results["master_address_support"] = {"result": master_address_support, "message": "File /launch.sh does contain SPARK_MASTER_ADDRESS"}

                entrypoint_present = fs.file_is_present('/entrypoint')
                results["entrypoint_present"] = {"result": entrypoint_present, "message": "File /entrypoint should be present on the image"}

                spark_home_present = fs.directory_is_present(resolved_spark_home)
                results["spark_home_present"] = {"result": spark_home_present, "message": "Directory /opt/spark should be present on the image"}

                if spark_home_present:
                    config_directory_present = fs.directory_is_present(resolved_spark_home + '/conf')
                    default_config_present = config_directory_present and fs.file_is_present(resolved_spark_home + '/conf/spark-defaults.conf')
                    spark_class_present = fs.file_is_present(resolved_spark_home + '/bin/spark-class')
                    release_file_present = fs.file_is_present(resolved_spark_home + '/RELEASE')
                else:
                    config_directory_present = default_config_present = spark_class_present = release_file_present = False

                results["config_directory_present"] = {"result": config_directory_present, "message": "Directory /opt/spark/conf/ is present on the image"}
                results["default_config_present"] = {"result": default_config_present, "message": "Default config spark-defaults.conf is on the right place"}
                results["spark_class_present"] = {"result": spark_class_present, "message": "File /opt/spark/bin/spark-class should be present on the image"}
                results["release_file_present"] = {"result": release_file_present, "message": "File /opt/spark/RELEASE should be present on the image"}


                print_result(results)

                if release_file_present:
                    print(colored("\n\nApache Spark info:", "yellow"))
                    print(fs.read_file(resolved_spark_home + '/RELEASE'))

                # todo:
                # print entrypoint
                # print command
                # print env
                # print labels
                # assert 'spark.ui.reverseProxy' in fs.read_file('/opt/spark/conf/spark-defaults.conf')
                # print("done.")
                # todo: container.http_request(7077..)
            
        finally:
            container.kill()
            container.delete()

def print_result(results):
    print("\n")
    all_ok = all(map(lambda r: r["result"], results.values()))
    if all_ok:
        print("Radley approves!")
        import os
        os.system("echo -e \"$(<radley.ascii)\" \\\\n")
        f = open(os.path.join(os.path.dirname(__file__), 'radley.ascii'), 'r')
        for line in f:
            print(line, end='')
        #os.system("img2txt.py ~/.Downloads/radley.png --ansi --targetAspect=0.4 --bgcolor=#ffffff --antialias --maxLen=80")
    else:
        print("\nThe image is not spark-operator compatible 👎")

    print("\n%s" % colored("RESULTS:", "yellow"))
    for key in results:
        print("[ %s ] ... %s" % (colored("✓", "green") if results[key]["result"] else colored("✕", "red"), results[key]["message"]))
    print("\n")

if __name__ == '__main__':
    check()
