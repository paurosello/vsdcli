vsdcli
========

CLI for VSD, the VSD Python SDK


Setting up your Python environment
----------------------------------

Install your virtualenv

    $ virtualenv vsdkcli-env

__Note__: If you are using a specific version of python, you can specify it using option `-p /usr/bin/python2.6` for instance.

Activate your environment

    $ cd vsdkcli-env
    $ source bin/activate # Activate your environment here...
    (vsdkcli-env) $ ...


Installation
------------

NOTE: If it is not the case, please activate your Python environment first!

    1) Install CLI dependencies

    (vsdkcli-env) $ pip install -r requirements.txt

    2) Make sure your `vsdcli` command is executable

    (vsdkcli-env) $ chmod +x vsdcli

Usage
-----

Follow the CLI help menu:

    (vsdkcli-env) $ ./vsdcli -h

Examples:

    (vsdkcli-env) $ ./vsdcli list enterprises --api https://135.227.220.152:8443 -username csproot --password csproot --enterprise csp

    (vsdkcli-env) $ export VSDK_PASSWORD=csproot
    (vsdkcli-env) $ export VSDK_USERNAME=csproot
    (vsdkcli-env) $ export VSDK_API_URL=https://135.227.220.152:8443
    (vsdkcli-env) $ export VSDK_ENTERPRISE=csp

    (vsdkcli-env) $ ./vsdcli list enterprises
    (vsdkcli-env) $ ./vsdcli list vports -in subnet a3db271b-b4ab-45a2-995e-971bf9e761bb
    (vsdkcli-env) $ ./vsdcli show domain --id 04850601-bebb-4b9b-acac-a31b455595a4

    (vsdkcli-env) $ ./vsdcli create zone -in domain 04850601-bebb-4b9b-acac-a31b455595a4 -p name='Test Zone' IPType=IPV4 numberOfHostsInSubnets=4 maintenanceMode=DISABLED
    (vsdkcli-env) $ ./vsdcli create enterprise -p name='My Company.com'

    (vsdkcli-env) $ ./vsdcli update enterprise -i 26f67b33-3601-4cdf-8ed0-fba7116d0200 -p name='Example'
    (vsdkcli-env) $ ./vsdcli update zone -i c4e96631-cfbc-4dcd-a4c3-b2937e5eab13 -p name='Danger Zone'


Available commands
------------------

Here are a list of available commands:
* `list`
* `show`
* `create`
* `update`
* `delete`