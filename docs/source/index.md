[Soit](https://pypi.org/project/soit/) is a CLI tool that verifies if a container image satisfies certain set of predicates and can be then
used as the custom image for the [spark-operator](https://github.com/radanalyticsio/spark-operator).

# Contents
* [Introduction](README)
* [Checks](checks)
* [License](LICENSE)


### Usage
```bash
λ pip3 install soit --user
λ soit --help
Usage: soit [OPTIONS]

  Simple verification tool that check the compatibility with Spark Operator

Options:
  -i, --image TEXT  Container image with Spark.
  -t, --tag TEXT    Specific tag of the image.
  -v, --verbose     Verbose output.
  -f, --full        Full mode including spawning master and worker and testing
                    if they can connect.
  -s, --silent      Do not output anything to standard output.
  --help            Show this message and exit.
```

### Basic Info
You can check the [introduction](README) section to see it in action. It can operate in the basic mode and in the full mode. The full mode contains some additional checks for the image that tests if the Spark master and worker can connecto to each other, while the basic mode contains tests that verify if the image has certain paths available on the file system, whether or not it has `Bash` and `curl` installed, etc. For full list of the checks, consult [Checks](checks).


### Contributions
The project is open-source and available on Git Hub in this [repository](https://github.com/Jiri-Kremser/spark-operator-image-tool). Feel free to either open an issue or send the pull request to make this tool
even better.

``` tip:: Make the soit part of your tool chain by running in the silent mode and rely on the return codes. To do that, add the -s or --silent switch
```