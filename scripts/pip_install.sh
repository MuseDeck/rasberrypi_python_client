#!/bin/bash

pip_args="--break-system-packages -i https://mirrors.aliyun.com/pypi/simple/"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <package_name>"
    exit 1
fi

your_package=$1

pip install $pip_args $your_package
