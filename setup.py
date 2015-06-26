import os
from setuptools  import setup

version = os.environ.get("VSD_CLI_VERSION", "0.0.1")

setup(
    name='vsdcli',
    version=version,
    author='Christophe Serafin',
    packages=['vsdcli'],
    author_email='christophe.serafin@nuagenetworks.net',
    description='VSD Command Line Interface',
    long_description=open('README.md').read(),
    install_requires=[line for line in open('requirements.txt')],
    license='TODO',
    url='https://github.com/nuagenetworks',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: Other/Proprietary License",
        "Environment :: Console",
        "Intended Audience :: Developers"
    ],
    entry_points={
        'console_scripts': [
            'vsd = vsdcli.vsd:main']
    },
)
