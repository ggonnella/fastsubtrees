from setuptools import setup, find_packages

def readme():
  with open('README.md') as f:
    return f.read()

import sys
if not sys.version_info[0] == 3:
  sys.exit("Sorry, only Python 3 is supported")

setup(name='fastsubtrees',
      version='1.2',
      description='Tree representation for fast queries of '+\
                  'the list of IDs of any subtree',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://github.com/ggonnella/fastsubtrees',
      keywords="bioinformatics genomics taxonomy trees",
      author='Giorgio Gonnella and Aman Modi and others (see CONTRIBUTORS)',
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
      scripts=['bin/fastsubtrees-construct',
               'bin/fastsubtrees-query',
               'bin/fastsubtrees-attributes-construct',
               'bin/fastsubtrees-attributes-query',
               'bin/fastsubtrees-add-subtree',
               'bin/fastsubtrees-delete-subtree'],
      zip_safe=False,
      test_suite="nose.collector",
      include_package_data=True,
      install_requires=['tqdm>=4.57.0', 'loguru>=0.5.1', 'docopt>=0.6.2',
        "schema>=0.7.4", "sh>=1.14.2", "PyYAML>=6.0", "ntmirror>=1.2"],
      tests_require=['nose'],
    )
