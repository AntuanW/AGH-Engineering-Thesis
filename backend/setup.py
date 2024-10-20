from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line and not line.startswith("#")]


setup(
    name="",
    version="0.0.1",
    author="Antoni Wójcik, Grzegorz Piśkorski, Zuzanna Olszówka, Bartłomiej Słupik",
    description="A system for supporting development of computer networking laboratory classes",
    packages=find_packages(include=["app", "app.*"]),
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "start-app=app.main:start",
        ]
    },
    python_requires=">=3.10",
)