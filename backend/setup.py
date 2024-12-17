from setuptools import setup, find_packages
import logging

def parse_requirements(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line and not line.startswith("#")]
    except FileNotFoundError:
        logging.error(f"{filename} not found!")
        exit(1)


setup(
    name="AGH-Engineering-Thesis-backend",
    version="0.0.1",
    author="Antoni Wójcik, Grzegorz Piśkorski, Zuzanna Olszówka, Bartłomiej Słupik",
    author_email="antoniwojcik@student.agh.edu.pl",
    url="https://github.com/AntuanW/AGH-Engineering-Thesis",
    description="A system for supporting development of computer networking laboratory classes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(
        include=[
            "app",
            "app.*"
        ]
    ),
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.12",
    package_data={
        "app": ["logging.yaml"],
        "app.visualization": ["icons/*"]
    },
    entry_points={
        "console_scripts": [
            "start-app=app.main:start",
        ]
    },
)