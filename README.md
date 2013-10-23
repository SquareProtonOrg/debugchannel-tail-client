debugchannel-tail-client
========================

tails files and publishes the result to debugchannel.
this project contains a file called dctail which when executed will tail a set of files specified in ~/.dctail.json and publish the chains to debug channels. each file can be published to a different channel.

INSTALL
=======
execute the install.sh script which will add the dctail to /usr/local/bin and generate config


USAGE
======
a configuration file '~/.dctail.json' is generated after the install process.
this file has the following format:
{
    "address": "http://192.168.2.158:1025",
    "apiKey": "someApiKey",
    "files": {"/var/log/mylog.txt": "serverlog"}
}

address: server address of debuchannel.
apiKey: currently unused, this can have any value
files: maps files to tail to the channel to publish them on. 
in this example the mylog.txt file will be tailed and published onto channel serverlog at http://192.168.2.158:1025/serverlog

The command dctail(Debug Channel Tail) will parse this config file and start tailing these files. dctail can take command line arguments in the following form:
    dctail [ --setup | file1:channel1 [file2:channel2 [..]]]
    
    --setup: creates the ~/.dctail.json config file from defaults and then exits
    fileN:channelN will watch fileN and publish changes to channelN.


