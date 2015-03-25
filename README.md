vsdcli
========

CLI for VSD Nuage


Setting up your Python environment
----------------------------------

Install your virtualenv

    $ virtualenv vsdcli-env

__Note__: If you are using a specific version of python, you can specify it using option `-p /usr/bin/python2.6` for instance.

Activate your environment

    $ cd vsdcli-env
    $ source bin/activate # Activate your environment here...
    (vsdcli-env) $ ...


Installation
------------

NOTE: If it is not the case, please activate your Python environment first!

    1) Install CLI dependencies

    (vsdcli-env) $ pip install -r requirements.txt

    2) Make sure your `vsdcli` command is executable

    (vsdcli-env) $ chmod +x vsdcli

Usage
-----

Follow the CLI help menu:

    (vsdcli-env) $ ./vsdcli -h

You can define following environments variables:

* `VSDCLI_USERNAME` user name
* `VSDCLI_PASSWORD` user password
* `VSDCLI_API_URL` API URL
* `VSDCLI_ENTERPRISE` Enterprise name

Examples:

    (vsdcli-env) $ vsdcli list enterprises --api https://135.227.220.152:8443 --username csproot --password csproot --enterprise csp

    (vsdcli-env) $ export VSDCLI_PASSWORD=csproot
    (vsdcli-env) $ export VSDCLI_USERNAME=csproot
    (vsdcli-env) $ export VSDCLI_API_URL=https://135.227.220.152:8443
    (vsdcli-env) $ export VSDCLI_ENTERPRISE=csp

    (vsdcli-env) $ vsdcli list enterprises
    (vsdcli-env) $ vsdcli list enterprises -f "name == 'My Company'"
    (vsdcli-env) $ vsdcli list enterprises -x ID name   # List name and ID only
    (vsdcli-env) $ vsdcli list enterprises -x ALL       # List all fields
    (vsdcli-env) $ vsdcli list vports --in subnet a3db271b-b4ab-45a2-995e-971bf9e761bb
    (vsdcli-env) $ vsdcli show domain --id 04850601-bebb-4b9b-acac-a31b455595a4

    (vsdcli-env) $ vsdcli create zone --in domain dd960a1f-b555-4e6c-9bf5-f88832679b5e -p name='Test Zone' IPType=IPV4 numberOfHostsInSubnets=4 maintenanceMode=DISABLED
    (vsdcli-env) $ vsdcli create enterprise -p name='My Company'

    (vsdcli-env) $ vsdcli update enterprise -i 26f67b33-3601-4cdf-8ed0-fba7116d0200 -p name='Example'
    (vsdcli-env) $ vsdcli update zone -i c4e96631-cfbc-4dcd-a4c3-b2937e5eab13 -p name='Danger Zone'

    (vsdcli-env) $ vsdcli objects                           # List all objects
    (vsdcli-env) $ vsdcli objects -f nsg                    # List all objects that contains word nsg
    (vsdcli-env) $ vsdcli objects -p enterprise             # List all objects that have an enterprise as parent
    (vsdcli-env) $ vsdcli objects -c domain                 # List all objects that have a domain as child
    (vsdcli-env) $ vsdcli objects -p enterprise -c domain   # List all objects that have an enterprise as parent and a domain as child


Available commands
------------------

Here are a list of available commands:
* `list`
* `show`
* `create`
* `update`
* `delete`
* `objects` will enable you to traverse VSD objects hierarchy