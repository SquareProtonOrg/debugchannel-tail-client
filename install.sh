#! /bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp "${dir}/src/dctail" /usr/local/bin/
dctail > /dev/null 2>&1
