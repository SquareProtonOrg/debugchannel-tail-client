#! /bin/bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p /etc/debugchannel/

cp "${dir}/src/dctail.conf" /etc/debugchannel/dctail.conf
cp "${dir}/src/dctail.conf.sample" /etc/debugchannel/dctail.conf.sample
cp "${dir}/src/dctail" /usr/local/bin/
