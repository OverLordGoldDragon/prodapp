import os
import re
from setuptools import setup, find_packages

current_path = os.path.abspath(os.path.dirname(__file__))


def read_file(*parts):
    with open(os.path.join(current_path, *parts), encoding='utf-8') as reader:
        return reader.read()


def get_requirements(*parts):
    with open(os.path.join(current_path, *parts), encoding='utf-8') as reader:
        return list(map(lambda x: x.strip(), reader.readlines()))


def find_version(*file_paths):
    version_file = read_file(*file_paths)
    version_matched = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                version_file, re.M)
    if version_matched:
        return version_matched.group(1)
    raise RuntimeError('Unable to find version')


setup(
    name="prodapp",
    version=find_version('prodapp', '__init__.py'),
    packages=find_packages(),
    url="https://github.com/OverLordGoldDragon/prodapp",
    license="MIT",
    author="OverLordGoldDragon",
    author_email="16495490+OverLordGoldDragon@users.noreply.github.com",
    description="Score yourself.",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    keywords=(
        "productivity productivity-booster productivity-timer python-dash python"
    ),
    install_requires=get_requirements('requirements.txt'),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
