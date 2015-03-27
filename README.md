vsp
========

CLI for VSD Nuage


Setting up your Python environment
----------------------------------

Install your virtualenv

    $ virtualenv vsp-env

__Note__: If you are using a specific version of python, you can specify it using option `-p /usr/bin/python2.6` for instance.

Activate your environment

    $ cd vsp-env
    $ source bin/activate # Activate your environment here...
    (vsp-env) $ ...


Installation
------------

NOTE: If it is not the case, please activate your Python environment first!

    1) Install CLI dependencies

    (vsp-env) $ pip install -r requirements.txt

    2) Make sure your `vsp` command is executable

    (vsp-env) $ chmod +x vsp

Usage
-----

Follow the CLI help menu:

    (vsp-env) $ ./vsp -h

You can define following environments variables:

* `vsp_USERNAME` user name
* `vsp_PASSWORD` user password
* `vsp_API_URL` API URL
* `vsp_ENTERPRISE` Enterprise name

Examples:

    (vsp-env) $ vsp list enterprises --api https://vsd:8443 --username csproot --password csproot --enterprise csp --version 3.2

    (vsp-env) $ export vsp_PASSWORD=csproot
    (vsp-env) $ export vsp_USERNAME=csproot
    (vsp-env) $ export vsp_API_URL=https://vsd:8443
    (vsp-env) $ export vsp_ENTERPRISE=csp
    (vsp-env) $ export vsp_API_VERSION=3.2

    (vsp-env) $ vsp list enterprises
    (vsp-env) $ vsp list enterprises -f "name == 'My Company'"
    (vsp-env) $ vsp list enterprises -x ID name   # List name and ID only
    (vsp-env) $ vsp list enterprises -x ALL       # List all fields
    (vsp-env) $ vsp list vports --in subnet a3db271b-b4ab-45a2-995e-971bf9e761bb
    (vsp-env) $ vsp show domain --id 04850601-bebb-4b9b-acac-a31b455595a4

    (vsp-env) $ vsp create zone --in domain dd960a1f-b555-4e6c-9bf5-f88832679b5e -p name='Test Zone' IPType=IPV4 numberOfHostsInSubnets=4 maintenanceMode=DISABLED
    (vsp-env) $ vsp create enterprise -p name='My Company'

    (vsp-env) $ vsp update enterprise -i 26f67b33-3601-4cdf-8ed0-fba7116d0200 -p name='Example'
    (vsp-env) $ vsp update zone -i c4e96631-cfbc-4dcd-a4c3-b2937e5eab13 -p name='Danger Zone'

    (vsp-env) $ vsp objects                           # List all objects
    (vsp-env) $ vsp objects -f nsg                    # List all objects that contains word nsg
    (vsp-env) $ vsp objects -p enterprise             # List all objects that have an enterprise as parent
    (vsp-env) $ vsp objects -c domain                 # List all objects that have a domain as child
    (vsp-env) $ vsp objects -p enterprise -c domain   # List all objects that have an enterprise as parent and a domain as child


Available commands
------------------

Here are a list of available commands:
* `list`
* `show`
* `create`
* `update`
* `delete`
* `objects` will enable you to traverse VSD objects hierarchy