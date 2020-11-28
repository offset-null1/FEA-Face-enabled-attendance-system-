from setuptools import setup

setup(
    name = 'app',
    packages=['base.py','viz/viz.py'],
    include_package_data=True,
    install_requires=['flask','plotly'],
)