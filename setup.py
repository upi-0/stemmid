from setuptools import setup, find_packages

setup(
    name='stemmid',
    version='0.1',
    packages=find_packages(),
    include_package_data=True, 
    package_data={
        'stemmid': ['data/kd.txt'],
    },
    install_requires=[
        'more_itertools>=5.0.0',
    ],
    description='Stemming kata berbahasa indonesia',
    author='Luthfi Malik',
    author_email='kaplingtumbal@gmail.com',
)
