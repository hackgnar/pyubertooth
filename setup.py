import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyubertooth',
    version='0.2',
    author='Ryan Holeman',
    description='Pure Python Library for Ubertooth',
    maintainer='Haim Daniel',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/haim0n/pyubertooth',
    packages=setuptools.find_packages(),
    scripts=[
        'bin/pyubertooth_dump',
        'bin/pyubertooth_rx'
    ],
    install_requires=[
        'pyusb',
    ],
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ),
)
