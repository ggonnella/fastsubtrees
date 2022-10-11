# Genomes Attributes Viewer

Genomes Attributes Viewer is an example application that is 
built on top of fastsubtrees to depict its usage. The application 
consists of a comparison page to compare the attributes like genome size or 
GC content for two or more organisms. 

## Setup

The example application is present inside the source code of the 
fastsubtrees library and can be accessed under the `genome-attribute-viewer` directory.
Once the installation is finished the user has to run the scripts, `setup.py` which first creates a
tree file that contains the node ids and then generates a text file that
contains the scientific names of organisms along with their taxonomy 
ids and finally it creates attribute files for genome size and GC Content.

## Usage

To start the web application use the `start.py` script.
The application is available at the URL http://0.0.0.0:8050/ .

In the home page of the web application, the user can select an attribute,
which can either be genome size or GC content from the `Select Attribute` dialog
box. After selecting the attribute, one has to search for an organism
using either its name or taxonomy id given dialog box. More
organisms for comparison can be added by clicking the `Add Taxon` button.
Finally to generate the graphs and compare two or more organisms,
click the `Compare` button.

  

