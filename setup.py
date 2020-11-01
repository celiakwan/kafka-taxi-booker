from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name = 'kafka-taxi-booker',
    version = '0.0.1',
    author = 'Celia',
    description = 'Data streaming example',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    license = 'MIT License',
    packages = find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)