from setuptools import setup, find_packages

setup(
    name='gym_cloudsimplus',
    version='0.0.4',
    install_requires=['gym', 'py4j', 'numpy'],
    packages=find_packages()
)
