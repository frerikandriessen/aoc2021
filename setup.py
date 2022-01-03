from distutils.core import setup

setup(
    name="AoC cli",
    version="0.1",
    description="Advent of Code cli",
    author="Frerik Andriessen",
    author_email="f.d.andriessen@gmail.com",
    packages=["aoc"],
    install_requires=[
        "requests",
        "black",
        "mypy",
        "flake8",
    ],
    entry_points={"console_scripts": ["aoc=aoc.__main__:main"]},
)
