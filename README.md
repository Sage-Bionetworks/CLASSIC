# ReadMe

The Consortium for Longitudinal Behavioral and Social Science Data Integration and Coordination (CLASSIC) (U24AG081810) is an NIH-funded initiative that facilitates and stimulates collaboration among deeply phenotyped longitudinal studies of aging.

This repository is currently for internal, private use by Sage Bionetworks.

This repository contains draft files that are being edited by the assigned data manager for the CLASSIC OpenDrawer Portal. Final revised files will be uploaded to the `model` folder when ready.

# To view the data model in Google Sheets

1. [Data Model](https://docs.google.com/spreadsheets/d/1nPqZvSdzWbtT78D6dA3knpdTvNamahy-xASoA16n8ew/edit?usp=sharing)

2. [Metadata Template](https://docs.google.com/spreadsheets/d/1Negf_XoDv29OjXrNXxyhsL2TKTsyRbRY/edit?usp=sharing&ouid=114808658189033289995&rtpof=true&sd=true)

# Data Models

1. Tier 1 - Study Identity & Discovery: Make the study discoverable and uniquely identifiable; provide the minimum context needed to understand “what this is” and relate it to other studies/collections.	Low (usually already known; low sensitivity)
   
2. Tier 2 - Governane, Access & Provenance:	Let users understand whether and how the dataset can be accessed and reused (policy + operational access steps), without needing back-and-forth.	Low - Medium (often shareable, but sometimes requires coordination with governance teams. Often easy if links exist; harder if docs are scattered; generally safe to share)	The metadata contribution team can add additional metadata fields to each tab as needed. These metadata may be specific to a study or may be incorporated into the CLASSIC data model over time.

3. Tier 3 - Cohort & Population: Describe who is in the study and how the cohort was defined/ascertained, enough for a user to judge relevance before requesting access.	Medium (may require harmonizing terminology; some attributes may be sensitive or restricted → may keep optional where needed)	The metadata contribution team can add additional metadata fields to each tab as needed. These metadata may be specific to a study or may be incorporated into the CLASSIC data model over time.
   
4. Tier 4 - Study Design & Time:	Describe when and how often data were collected (longitudinal structure, bursts, waves, follow-up intervals, timestamp availability). This is key for interpretation and longitudinal/APC use cases.	Medium (sometimes requires pulling info from protocol/ops docs; typically shareable)	The metadata contribution team can add additional metadata fields to each tab as needed. These metadata may be specific to a study or may be incorporated into the CLASSIC data model over time.
   
5. Tier 5 - Measures & Instruments:	Describe what was measured (constructs, instrument identity, administration modality/technology) at a level that supports discovery and basic interpretability.	Medium - High (depends on how well instruments are documented and whether devices/platform info is centralized)	The metadata contribution team can add additional metadata fields to each tab as needed. These metadata may be specific to a study or may be incorporated into the CLASSIC data model over time
   
6. Tier 6 - Derived Scores, Variables & Availability Summaries:	Make derived outputs interpretable (what a score/variable represents, and its general derivation form), especially when item/trial-level data aren’t shared. Help users answer “is there enough data for my question?” without accessing participant-level files, counts, ranges, units, or timepoint-scoped summaries.	High (often requires analyst input or codebook review, requires computing/curating summaries; may be restricted depending on policy→ may keep optional/add to study later, i.e., "enrichment".	The metadata contribution team can add additional metadata fields to each tab as needed. These metadata may be specific to a study or may be incorporated into the CLASSIC data model over time.
			
Instructions	

How to start	

"Contribute in tiers. Every study should aim to complete Core. Enhanced and Deep add interpretability and reduce back-and-forth, but may have optional or ""null"" metadata.

Recommended “null reason” pattern (use anywhere a value is missing)

For any field that can’t be provided, either the Sage Team or the metadata contribution team will record a nullReason (or equivalent) using one of:

- Not collected
- Not available
- Not yet curated
- Not shared due to restrictions
- Unknown

1) Core: Start with Modules 1–2 (baseline minimum, lowest burden).

2) Enhanced: Add Modules 3–4 next (makes the dataset meaningfully interpretable).

3) Deep: Treat Modules 5–6 as “measure-level enrichment”. Use as the “DUA decision support” tier (most helpful but most work).


This repository contains 3 major files:

1. `example.model.csv`: The CSV representation of the example data model. This file is created by the collective effort of data curators and annotators from a *community* (e.g. *HTAN*), and will be used to create a JSON-LD representation of the data model.


2. `example.model.jsonld`: The JSON-LD representation of the example data model, which is automatically created from the CSV data model using the schematic CLI. More details on how to convert the CSV data model to the JSON-LD data model can be found [here](https://sage-schematic.readthedocs.io/en/develop/cli_reference.html#schematic-schema-convert). This is the central schema (data model) which will be used to power the generation of metadata manifest templates for various data types (e.g., `scRNA-seq Level 1`) from the schema.


3. `config.yml`: The schematic-compatible configuration file, which allows users to specify values for application-specific keys (e.g., path to Synapse configuration file) and project-specific keys (e.g., Synapse fileview for community project). A description of what the various keys in this file represent can be found in the [Fill in Configuration File(s)](https://sage-schematic.readthedocs.io/en/develop/README.html#fill-in-configuration-file-s) section of the schematic [docs](https://sage-schematic.readthedocs.io/en/develop/index.html).
