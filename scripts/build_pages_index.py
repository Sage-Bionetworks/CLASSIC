#!/usr/bin/env python3
"""Build ``docs/data.json`` for the GitHub Pages data-model index.

Merges two sources of truth:
  * Local schema files (``model/Tier */*.schema.json``) -> tier, title,
    description, property count, and the in-repo source path.
  * Synapse (the ``org.synapse.classic`` organization) -> schema id, latest
    semantic version, and creation metadata.

If a Synapse token is unavailable (``SYNAPSE_AUTH_TOKEN`` unset and no usable
``~/.synapseConfig``) the script still emits a file from local data alone, with
version/id left as null, so the page can render in any environment.

Output: ``docs/data.json`` consumed by ``docs/index.html``.
"""

import asyncio
import glob
import json
import os
import re
from datetime import datetime, timezone
from urllib.parse import quote

ORG = "org.synapse.classic"
REPO = "Sage-Bionetworks/CLASSIC"
BRANCH = "main"
SCHEMA_GLOB = "model/Tier */*.schema.json"
OUT_PATH = os.path.join("docs", "data.json")
SEMVER_RE = re.compile(r"^\s*v?(\d+)\.(\d+)\.(\d+)\s*$")


def schema_name_from_id(schema_id: str) -> str:
    marker = f"registered/{ORG}-"
    idx = schema_id.find(marker)
    if idx == -1:
        raise ValueError(f"$id '{schema_id}' missing 'registered/{ORG}-' prefix")
    return schema_id[idx + len(marker):]


def tier_from_path(path: str):
    m = re.search(r"Tier[ _](\d+)", path)
    return int(m.group(1)) if m else None


def parse_semver(value):
    if value is None:
        return None
    m = SEMVER_RE.match(str(value))
    return tuple(int(p) for p in m.groups()) if m else None


def read_local_schemas():
    """Return {schema_name: {...}} from the local .schema.json files."""
    out = {}
    for path in sorted(glob.glob(SCHEMA_GLOB)):
        with open(path, encoding="utf-8") as fh:
            body = json.load(fh)
        name = schema_name_from_id(body["$id"])
        rel = path.replace("\\", "/")
        # Encode path segments (folders contain spaces) so the links resolve.
        rel_url = "/".join(quote(seg) for seg in rel.split("/"))
        out[name] = {
            "tier": tier_from_path(path),
            "title": body.get("title", name),
            "description": body.get("description", ""),
            "name": name,
            "uri": f"{ORG}-{name}",
            "properties": len(body.get("properties", {})),
            "required": body.get("required", []),
            "source": rel,
            "source_url": f"https://github.com/{REPO}/blob/{BRANCH}/{rel_url}",
            "raw_url": f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{rel_url}",
            "version": None,
            "schema_id": None,
            "created_on": None,
            "created_by": None,
        }
    return out


async def enrich_from_synapse(schemas: dict) -> bool:
    """Fill in version/id/created_* from Synapse. Returns True if it ran."""
    token = os.environ.get("SYNAPSE_AUTH_TOKEN")
    try:
        from synapseclient import Synapse
        from synapseclient.models import SchemaOrganization
    except Exception:
        return False

    syn = Synapse()
    try:
        if token:
            syn.login(authToken=token)
        else:
            syn.login()  # fall back to ~/.synapseConfig
    except Exception as exc:
        print(f"WARN: Synapse login failed, emitting local-only index: {exc}")
        return False

    org = SchemaOrganization(ORG)
    async for js in org.get_json_schemas_async(synapse_client=syn):
        entry = schemas.get(js.name)
        if entry is None:
            continue
        entry["schema_id"] = js.id
        entry["created_on"] = js.created_on
        entry["created_by"] = js.created_by
        latest = None
        async for info in js.get_versions_async(synapse_client=syn):
            for attr in ("semantic_version", "semanticVersion", "version", "version_number"):
                parsed = parse_semver(getattr(info, attr, None))
                if parsed and (latest is None or parsed > latest):
                    latest = parsed
        if latest is not None:
            entry["version"] = ".".join(map(str, latest))
    return True


async def main():
    schemas = read_local_schemas()
    if not schemas:
        raise SystemExit(f"No schema files matched '{SCHEMA_GLOB}'")

    enriched = await enrich_from_synapse(schemas)

    rows = sorted(schemas.values(), key=lambda r: (r["tier"] is None, r["tier"], r["name"]))
    payload = {
        "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "organization": ORG,
        "repo": REPO,
        "branch": BRANCH,
        "source": "synapse+local" if enriched else "local-only",
        "schema_endpoint": "https://repo-prod.prod.sagebase.org/repo/v1/schema/type/registered/",
        "schemas": rows,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"Wrote {OUT_PATH}: {len(rows)} schema(s), source={payload['source']}")


if __name__ == "__main__":
    asyncio.run(main())
