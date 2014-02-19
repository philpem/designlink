try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='DesignLink',
	version='0.1.0',
	author='Phil Pemberton',
	author_email='philpem.me.uk',
	packages=['designlink'],
	url='http://pypi.python.org/pypi/DesignLink/',
	license='LICENSE.txt',
	description='Python wrapper for the Farnell DesignLink SOAP API',
	long_description=open('README.txt').read(),
	
	classifiers=[
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: MIT License",
		"Topic :: Internet",
		"Intended Audience :: Developers",
		"Natural Language :: English",
		"Operating System :: OS Independent",
	],

	install_requires=[
		"suds-jurko >= 0.6",
	],
)

