## spark-operator-image-tool
[![Build status](https://travis-ci.org/Jiri-Kremser/spark-operator-image-tool.svg?branch=master)](https://travis-ci.org/Jiri-Kremser/spark-operator-image-tool)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![PyPI version](https://badge.fury.io/py/soit.svg)](https://pypi.org/project/soit/)
[![Docs](https://readthedocs.org/projects/spark-operator-image-tool/badge/?version=latest)](https://spark-operator-image-tool.readthedocs.io/en/latest/?badge=latest)


Purpose of this tool is to verify if given container image is compatible with [spark-operator](https://github.com/radanalyticsio/spark-operator).

### Installation

```
pip3 install soit --user
```

### Quick Start

```
soit --image quay.io/jkremser/openshift-spark --tag 2.4.0
```

#### Demo

<!--
asciinema rec -i 3
docker run -\-rm -v $PWD:/data asciinema/asciicast2gif -s 1.18 -S 3 -h 62 -t monokai 189204.cast demo.gif
-->
[![Watch the full asciicast](https://github.com/Jiri-Kremser/spark-operator-image-tool/raw/master/ascii.gif)](https://asciinema.org/a/238399?&cols=123&rows=63)

#### Local Development

Install the modules:

```
pip3 install -r requirements.txt --user
```

Run the app:

```
python3 soit/main.py
```

#### Other
This tool is based on a library for interactive testing of container images called [conu](https://github.com/user-cont/conu).
