import importlib.util
import os.path
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as readme_file:
    README = readme_file.read()


DESCRIPTION = "Tools for integrating Falcon applications with Firebase."

REQUIRES = ["falcon >= 2.0.0", "firebase_admin >= 4.0.0", "pydantic >= 1.0.0"]


setup(
    name="firefalcon",
    version="0.0.3",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zqwalker/firefalcon",
    author="Zackary Walker",
    author_email="quinn@soarbi.com",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="falcon middleware firebase firestore authentication",
    packages=['firefalcon'],
    python_requires=">=3.8",
    install_requires=REQUIRES,
    include_package_data=True,
)