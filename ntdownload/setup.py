#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
from setuptools import setup, find_packages

def readme():
  with open('README.md') as f:
    return f.read()

import sys
if not sys.version_info[0] == 3:
  sys.exit("Sorry, only Python 3 is supported")

setup(name='ntdownload',
      version='1.7.1',
      description="Easily updatable local NCBI taxonomy dumps file copy",
      long_description=readme(),
      long_description_content_type="text/markdown",
      install_requires=["loguru", "snacli", "schema"],
      url='https://github.com/ggonnella/fastsubtrees/tree/main/ntdowload',
      keywords="ncbi taxonomy dumpfiles mirror",
      author='Giorgio Gonnella',
      author_email='gonnella@zbh.uni-hamburg.de',
      license='ISC',
      # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
      ],
      packages=find_packages(),
      scripts=['bin/ntdownload', 'bin/ntnames'],
      zip_safe=False,
      test_suite="pytest",
      include_package_data=True,
      tests_require=['pytest', 'pytest-console-scripts', 'sh'],
    )
