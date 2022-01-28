"""Setup configuration and dependencies for rom24."""

from setuptools import find_packages  # type: ignore
from setuptools import setup


REQUIREMENTS = [requirement for requirement in open("requirements.txt").readlines()]

COMMANDS = ["rom24=rom24.pyom:pyom"]

setup(
    name="rom24",
    version="0.0.1.alpha2",
    author="Micheal Taylor",
    author_email="bubthegreat@gmail.com",
    url="",
    include_package_data=True,
    description="Attempt at properly packaging rom24 python.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.6.6",
    entry_points={"console_scripts": COMMANDS},
    install_requires=REQUIREMENTS,
)
