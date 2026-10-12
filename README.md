# CLASSIC Metadata Model

The Consortium for Longitudinal Behavioral and Social Science Data Integration and Coordination (CLASSIC; U24AG081810) is an NIH-funded initiative supporting collaboration among deeply phenotyped longitudinal studies of aging.

This repository maintains the tiered metadata model for the CLASSIC OpenDrawer Portal. The model supports discovery of studies, understanding of their populations and measures, and identification of data access and reuse requirements. The portal describes studies and available data; access to underlying research data follows the procedures established by each data provider.

## Start here

- **Browse the model:** Open the [CLASSIC data model index](https://sage-bionetworks.github.io/CLASSIC/) to explore tiers, field descriptions, required fields, and permitted values.
- **Review the operational schemas:** Use the JSON schemas in [model/](model/). The schemas in `model/Tier 1/` through `model/Tier 5/` are the files selected by the Synapse registration script.
- **Review the LinkML model:** Use [model/linkml/](model/linkml/) for tier definitions, shared fields, and controlled vocabularies.
- **Propose a change:** Open a [GitHub issue](https://github.com/Sage-Bionetworks/CLASSIC/issues) or pull request describing the affected field and study use case.

**GitHub is the source of truth for the metadata model.** The earlier Google Sheets data model and metadata template are historical references. Consult the current repository schemas for field names, definitions, required fields, and permitted values.

## Metadata tiers

The current model contains five tiers. Measures, instruments, derived scores, variables, and availability summaries are combined in Tier 5.

| Tier | Scope | Purpose |
| --- | --- | --- |
| [1](model/Tier%201/) | Study Identity & Discovery | Identify the study and provide the context needed to discover it and relate it to other studies or collections. |
| [2](model/Tier%202/) | Governance, Access & Provenance | Describe governance, consent, data use restrictions, where data are hosted, and how researchers can request access. |
| [3](model/Tier%203/) | Cohort & Population | Describe the population, eligibility criteria, recruitment, and cohort characteristics. |
| [4](model/Tier%204/) | Study Design & Time | Describe study design, waves, bursts, and the timing and frequency of data collection. |
| [5](model/Tier%205/) | Measures, Instruments, Derived Scores, Variables & Availability Summaries | Describe what was measured, how instruments were administered, how outputs were derived, and the data available for research. |

Contributions can be developed progressively: begin with study identity and governance information, add population and design information, then enrich measure-level metadata. Required fields are defined by each schema; this progression does not replace those requirements.

## Repository contents

| Location | Contents |
| --- | --- |
| `model/Tier 1/`–`model/Tier 5/` | Tier JSON schemas used by the Synapse registration workflow. |
| [model/linkml/classic.yaml](model/linkml/classic.yaml) | Umbrella LinkML schema importing the shared core and all five tiers. |
| [model/linkml/classic_core.yaml](model/linkml/classic_core.yaml) | Shared identifiers, scope fields, mixins, and controlled vocabularies. |
| `model/linkml/tier*.yaml` | Individual LinkML tier definitions. |
| `model/linkml/tier*.schema.json` | JSON Schema representations alongside the LinkML definitions. |
| [docs/](docs/) | Schema browser and its metadata index, `data.json`. |
| [scripts/register_synapse_schemas.py](scripts/register_synapse_schemas.py) | Registers tier JSON schemas in Synapse with semantic versions. |
| [scripts/build_pages_index.py](scripts/build_pages_index.py) | Builds the browser index from local tier schemas and, when available, Synapse registration metadata. |
| [draft model/](draft%20model/) | Working drafts; use the schemas in `model/` for current tier definitions. |

The two sets of JSON schemas serve different representations of the model. Do not assume that the files under `model/linkml/` are interchangeable with the operational tier schemas. Changes should be reviewed across both representations.

## Preparing metadata

1. Review the relevant tier schema and its field descriptions before filling in metadata.
2. Use a stable `studyID` to connect records for the same study. Preserve identifiers when study names or other descriptive information change.
3. Where applicable, use cohort, measure, row identifiers, and scope fields to indicate what a record describes. Follow the field names and permitted values in the schema used for the submission.
4. Match controlled vocabulary values exactly. Follow the schema's data types and cardinality rather than assuming a field accepts multiple values.
5. Follow the schema's handling of missing values. Use values such as `Unknown` only where permitted; use JSON `null` only where the schema allows it. Do not introduce undocumented placeholder values or fields.
6. Flag missing terms or unclear definitions for review rather than adding new columns to the shared model without a schema change.

### Access and reuse metadata

Tier 2 separates several aspects of access:

- `accessRestrictions` records controlled terms describing permitted research uses and restrictions.
- `dataUseConditions` provides additional free-text context about data use conditions.
- `accessRequirements`, `accessProcedure`, `accessRequestURL`, and `accessReviewBody` describe requirements and the access request process.

Record restrictions from the provider's documented terms. If a restriction is ambiguous—for example, whether methods research includes a particular psychometric validation activity—seek clarification from the provider or access review body. Metadata summarizes those terms; it does not independently authorize research use.

## Updating the model

Submit changes through a pull request with the reason for the change, affected tiers, and examples of metadata that should pass or fail validation.

When changing a field or controlled vocabulary:

1. Update the operational tier JSON schema under `model/Tier N/`.
2. Update the corresponding LinkML tier definition. Shared vocabulary changes belong in `model/linkml/classic_core.yaml`.
3. Update the corresponding JSON Schema representation under `model/linkml/` and check consistency across the affected files.
4. Check syntax and schema validity, and validate representative records against the operational schema.
5. Document compatibility implications. Renaming a permitted value may require updating existing metadata annotations and templates.

The registration workflow does **not** generate JSON schemas from LinkML. Keep the affected representations synchronized in the same pull request. LinkML `todos` and commented rule examples describe planned work; they are not active validation rules.

For validation suggestions, use the repository's **Schema Validation Rule Suggestion** issue template and include the attribute, proposed rule, importance, and expected use case.

## Synapse registration and schema browser updates

The [Register Synapse Schemas workflow](.github/workflows/register-synapse-schemas.yml) runs when matching schema or workflow-related changes land on `main`. It can also be started manually from the repository's Actions tab.

- The registration script selects `model/Tier */*.schema.json` by default and publishes schemas in the Synapse organization `org.synapse.classic`.
- New schemas start at version `1.0.0` by default. Unchanged schema bodies are skipped; changed bodies receive a patch increment by default. Manual runs can select a minor or major increment or a dry run.
- Registration requires the repository secret `SYNAPSE_AUTH_TOKEN` with appropriate schema registration permissions.
- After a publishing run, the workflow rebuilds `docs/data.json` and opens a pull request when the index changes. Merge that pull request to incorporate the refreshed index into `main`.

The browser displays a generated snapshot. Consult the repository schemas for the latest merged definitions and check workflow results to confirm publication. YAML-only changes do not trigger schema registration, and the workflow does not generate contributor spreadsheet templates.

## License

Repository materials are distributed under the [MIT License](LICENSE). Research data described by the model remain subject to their own access and use terms.
