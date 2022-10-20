from setuptools import setup, find_packages

import sys
if not sys.version_info[0] == 3:
  sys.exit("Sorry, only Python 3 is supported")

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='ntsubtree',
      version='1.1',
      description='Tree representation for fast queries of '+\
                   'the subtree of a taxon in the NCBI taxonomy tree',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url="https://github.com/ggonnella/fastsubtrees/tree/main/ntsubtree",
      keywords="bioinformatics genomics taxonomy trees",
      author='Giorgio Gonnella and and others (see CONTRIBUTORS)',
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
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries',
      ],
      packages=find_packages(),
      scripts=['bin/ntsubtree'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['tqdm>=4.57.0', 'loguru>=0.5.1', 'docopt>=0.6.2',
        "schema>=0.7.4", "sh>=1.14.2",
        "ntdownload", "fastsubtrees", "PlatformDirs"],
      setup_requires=['PlatformDirs'],
      test_suite="pytest",
      tests_require=['pytest', 'pytest-console-scripts', 'sh'],
    )
