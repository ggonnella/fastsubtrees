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

setup(name='genomes_attributes_viewer',
      version='1.3',
      description="Example application of fastsubtrees",
      long_description=readme(),
      long_description_content_type="text/markdown",
      install_requires=["fastsubtrees>=2.0", "ntdownload", "dash==2.0.0",
        "dash-bootstrap-components==1.0.2", "dash-core-components==2.0.0",
        "dash-html-components==2.0.0", "dash-table==5.0.0", "Werkzeug==2.0.0",
        "Flask==2.1.2", "pandas"],
      url='https://github.com/ggonnella/fastsubtrees/"+\
            "tree/main/genomes_attributes_viewer',
      keywords="ncbi taxonomy webapp dash fastsubtrees",
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
      package_data={'genomes_attributes_viewer':
        ['data/accession_taxid_attribute.tsv.gz']},
      scripts=['bin/genomes-attributes-viewer'],
      zip_safe=False,
      include_package_data=True,
    )
