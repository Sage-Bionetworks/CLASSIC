# ReadMe

This repository is currently for internal, private use by Sage Bionetworks.

This repository contains draft files that are being edited by the assigned data manager for the CLASSIC OpenDrawer Portal. Final revised files will be uploaded to the `model` folder when ready.

# To view the data model in Google Sheets

1. [Data Model](https://docs.google.com/spreadsheets/d/1nPqZvSdzWbtT78D6dA3knpdTvNamahy-xASoA16n8ew/edit?usp=sharing)

2. [Metadata Template](https://docs.google.com/spreadsheets/d/1Negf_XoDv29OjXrNXxyhsL2TKTsyRbRY/edit?usp=sharing&ouid=114808658189033289995&rtpof=true&sd=true)

# Data Models

This repository contains 3 major files:

1. `example.model.csv`: The CSV representation of the example data model. This file is created by the collective effort of data curators and annotators from a *community* (e.g. *HTAN*), and will be used to create a JSON-LD representation of the data model.


2. `example.model.jsonld`: The JSON-LD representation of the example data model, which is automatically created from the CSV data model using the schematic CLI. More details on how to convert the CSV data model to the JSON-LD data model can be found [here](https://sage-schematic.readthedocs.io/en/develop/cli_reference.html#schematic-schema-convert). This is the central schema (data model) which will be used to power the generation of metadata manifest templates for various data types (e.g., `scRNA-seq Level 1`) from the schema.


3. `config.yml`: The schematic-compatible configuration file, which allows users to specify values for application-specific keys (e.g., path to Synapse configuration file) and project-specific keys (e.g., Synapse fileview for community project). A description of what the various keys in this file represent can be found in the [Fill in Configuration File(s)](https://sage-schematic.readthedocs.io/en/develop/README.html#fill-in-configuration-file-s) section of the schematic [docs](https://sage-schematic.readthedocs.io/en/develop/index.html).
