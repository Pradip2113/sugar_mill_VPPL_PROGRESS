from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sugar_mill/__init__.py
from sugar_mill import __version__ as version

setup(
	name="sugar_mill",
	version=version,
	description="Sugar Mill",
	author="Quantbit",
	author_email="21pradipjadhav@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
