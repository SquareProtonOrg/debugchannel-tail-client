#! /bin/bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p /etc/debugchannel/

if [ ! -f /etc/debugchannel/dctail.conf ]; then
    cp "${dir}/src/etc-debugchannel-dctail.conf" /etc/debugchannel/dctail.conf
fi


cp "${dir}/src/etc-debugchannel-dctail.conf.sample" /etc/debugchannel/dctail.conf.sample
cp "${dir}/src/dctail" /usr/local/bin/
chmod 755 /usr/local/bin/dctail

cp "${dir}/src/etc-init.d-dctail" /etc/init.d/dctail
chmod 755 /etc/init.d/dctail
