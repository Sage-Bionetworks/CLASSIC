#!/usr/bin/env python3
"""Convert CLASSIC Tier field-catalog JSON files into Synapse-registrable
draft-07 JSON Schemas.

Source format (per file): { tier, id, name, purpose, fields: [ {name, data_type,
description, has_dropdown, valid_values:[{value, definition}]}, ... ] }

Target format: a draft-07 JSON Schema with $schema, $id (registered Synapse URI),
type=object, properties (keyed by field name), title, description, required.
"""

import json
import glob
import os

ORG = "org.synapse.classic"
BASE_ID = "https://repo-prod.prod.sagebase.org/repo/v1/schema/type/registered"

# Map tier number -> schema-name slug used in the registered $id.
# Synapse schema names must be period-separated sections; each section must
# start with a letter and contain only letters and numbers (no hyphens).
SLUGS = {
    1: "tier1.studyIdentityDiscovery",
    2: "tier2.governanceAccessProvenance",
    3: "tier3.cohortPopulation",
    4: "tier4.studyDesignTime",
    5: "tier5.measuresInstruments",
}

# Fields that anchor every row; treated as required. Adjust per study policy.
REQUIRED = ["studyID"]

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "model")


def build_property(field):
    """Translate one source field object into a JSON Schema property."""
    prop = {
        "type": "string",
        "title": field["name"],
        "description": field.get("description") or "",
    }
    if field.get("data_type") == "enum" and field.get("valid_values"):
        # Flatten {value, definition} -> value, dedupe while preserving order.
        seen = set()
        enum = []
        for vv in field["valid_values"]:
            v = vv.get("value")
            if v is not None and v not in seen:
                seen.add(v)
                enum.append(v)
        prop["enum"] = enum
    return prop


def convert(src_path):
    with open(src_path, encoding="utf-8") as fh:
        data = json.load(fh)

    tier = data["tier"]
    slug = SLUGS[tier]

    properties = {}
    for field in data["fields"]:
        properties[field["name"]] = build_property(field)

    # Only keep required fields that actually exist in this tier.
    required = [r for r in REQUIRED if r in properties]

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": f"{BASE_ID}/{ORG}-{slug}",
        "type": "object",
        "title": data.get("name", slug),
        "description": data.get("purpose", ""),
        "properties": properties,
        "required": required,
    }

    out_path = os.path.splitext(src_path)[0] + ".schema.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(schema, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"tier {tier}: {len(properties):>2} properties -> {os.path.basename(out_path)}")


def main():
    pattern = os.path.join(MODEL_DIR, "Tier *", "Tier_*.json")
    sources = [p for p in glob.glob(pattern) if not p.endswith(".schema.json")]
    for src in sorted(sources):
        convert(src)


if __name__ == "__main__":
    main()
