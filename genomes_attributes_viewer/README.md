# Genomes Attributes Viewer

Genomes Attributes Viewer is an example application that is 
built on top of fastsubtrees to depict its usage. The application 
consists of a comparison page to compare the attributes like genome size or 
GC content for two or more organisms. 

## Installation

The example application can be installed using ``pip install genome_attribute_viewer``.

## Starting the application

To start the web application use the `genomes-attribute-viewer` script.

On first run, preparation steps are run, which take about 13 seconds
(the NCBI Taxonomy dump files are downloaded from NCBI,
a tree file for fastsubtrees is generated, along files which
contains the scientific names of organisms and
faststubrees attribute files for genome size and GC content of bacterial genomes
using the provided example data).

On subsequent runs these steps are skipped.

The application is available, by default, at the URL http://0.0.0.0:8050/ .
The hostname and port can be set using the options ``--host`` and ``--port``
respectively.

## Usage

In the home page of the web application, the user can select an attribute,
which can either be genome size or GC content from the `Select Attribute` dialog
box. After selecting the attribute, one has to search for an organism
using either its name or taxonomy id given dialog box. More
organisms for comparison can be added by clicking the `Add Taxon` button.
Finally to generate the graphs and compare two or more organisms,
click the `Compare` button.

