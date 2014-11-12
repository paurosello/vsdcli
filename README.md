vsdk-cli
========

CLI for VSDK, the VSD Python SDK


Setting up your Python environment
----------------------------------

Install your virtualenv

    $ virtualenv --no-site-packages vsdkcli-env

Activate your environment

    $ cd vsdkcli-env
    $ source bin/activate
    (vsdkcli-env) $ ...


Installation
------------

NOTE: If it is not the case, please activate your Python environment first!

    1) Install Bambou and VSDK

    (pymodel-env) $ pip install git+ssh://github.mv.usa.alcatel.com/chserafi/bambou#egg=bambou
    (pymodel-env) $ pip install url_to_your_vsdk_.tar.gz

    2) Install CLI dependencies

    (pymodel-env) $ pip install -r requirements.txt

    3) Make sure your `vsdk-cli` command is executable

    (pymodel-env) $ chmod +x vsdk-cli

Usage
-----

Follow the CLI help menu:

    (pymodel-env) $ ./vsdk-cli -h

Examples:

    (pymodel-env) $ ./vsdk-cli list_enterprises --api https://135.227.220.152:8443/nuage/api/v3_0 -u csproot -p csproot --enterprise csp

    (pymodel-env) $ export VSDK_PASSWORD=csproot
    (pymodel-env) $ export VSDK_USERNAME=csproot
    (pymodel-env) $ export VSDK_API_URL=https://135.227.220.152:8443/nuage/api/v3_0
    (pymodel-env) $ export VSDK_ENTERPRISE=csp
    (pymodel-env) $ ./vsdk-cli list_enterprises


Available commands
------------------

Here are a list of available commands:
* `list_enterprises`
* `show_enterprise`