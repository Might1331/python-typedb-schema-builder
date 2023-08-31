from setuptools import setup, find_packages

setup(
    name="typedb-schema-builder",
    version="11.0.6",
    description = "typedb schema builder package",
    packages=find_packages(),
    install_requires=[
        "antlr4-python3-runtime==4.7.2"
    ],
    author="Pratap Singh",
    author_email="pratap.singh@vaticle.com",
    readme = "README.md",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    project_urls={
    "Homepage":"https://github.com/Might1331/python-typedb-schema-builder/",
    "Bug Tracker":"https://github.com/Might1331/python-typedb-schema-builder/issues",
    }
)
