debugchannel-tail-client
========================

A simple command line tool that can tail multiple files and publish the output to debugchannels.  This can be used for tailing mysql slow queries log, apache error logs or infact any log file which is related to your software development.

Install
=======
Execute the install.sh script (as root) which will add dctail to /usr/local/bin/ and generate config file /etc/debugchannel/dctail.conf.


Configuration
=============
The configuration file `/etc/debugchannel/dctail.conf` is generated during the install process.  The permission on the configuration file is set to 644 which allows the file to be read by any user but it can only be written by root.  This file has the following json format:

```
{
    "address": "http://192.168.2.158:1025",
    "apiKey": "someApiKey",
    "files": {"/var/log/mylog.txt": "nameofchannel"}
}
```

`address`: (required) server address of debugchannel. 

`apiKey`: (optional) set if your debugchannel supports authentication (only available on enterprise debugchannels)

`files`: (optional) maps files to debugchannels.  If you do not set a list of file in the configuration file then you will need to specify them when you run dctail from the command line.


Example Usage
=============
If you have specified a list of files in dctail.conf then you simple run:

```
   dctail
```

If you have not specified any files in dctail.conf then you can specify file the files in the command line:

```
    dctail mylog.txt:mylogchannel serverlog.txt:serverlogchannel
```

This will tail 2 files: `mylog.txt` and `serverlog.txt` and publish the results to the channels logchannel and serverlogchannel respectively. 

You can specify files in both the dctail.conf and as command line options and both will be used.  However, if there is conflict the command line arguments will overright the configuration specifed in the file.

If you have damaged your configuration file then you can run 

```
    dctail --setup
```

This creates the ~/.dctail.json config file from defaults and then exits
