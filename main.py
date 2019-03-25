import click
import logging, coloredlogs
# import daiquiri
from conu import DockerRunBuilder, DockerBackend

# daiquiri.setup(level=logging.INFO)
coloredlogs.install(level='DEBUG')



#python3 main.py --image quay.io/jkremser/openshift-spark --tag 2.4.0

# image = 'quay.io/jkremser/openshift-spark'
# tag = '2.4.0'
# backend = DockerBackend(logging_level=logging.DEBUG)

@click.command()
@click.option('--image', prompt='container image', help='Container image with Spark.')
@click.option('--tag', prompt='tag', default='latest', help='Specific tag of the image.')
def check(image, tag):
    """Simple verification tool that check the compatibility with Spark Operator"""
    with DockerBackend(logging_level=logging.DEBUG) as backend:
        # the image will be pulled if it's not present
        i = backend.ImageClass(image, tag=tag)

        # the command to run in a container
        run_params = DockerRunBuilder(additional_opts=['--entrypoint', ''], command=['sleep', '3600'])
        container = i.run_via_binary(run_params)

        assert container.is_running(), "Container must be running"
        try:
            # we can also access it directly on disk and compare
            with container.mount() as fs:
                print("1")
                assert fs.file_is_present('/launch.sh')
                print("2")
                launch_script = fs.read_file('/launch.sh')
                print("3")
                assert 'SPARK_METRICS_ON' in launch_script
                print("4")
                assert 'SPARK_MASTER_ADDRESS' in launch_script
                print("5")
                assert fs.file_is_present('/entrypoint')
                print("6")
                assert fs.directory_is_present('/opt/spark/bin')
                print("7")
                assert 'spark.ui.reverseProxy' in fs.read_file('/opt/spark/conf/spark-defaults.conf')
                print("done.")
                # todo: container.http_request(7077..)
        finally:
            container.kill()
            container.delete()

if __name__ == '__main__':
    check()
