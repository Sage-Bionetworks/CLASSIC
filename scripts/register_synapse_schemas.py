#!/usr/bin/env python3
"""Register CLASSIC tier JSON Schemas to Synapse with semantic versioning.

For every ``model/Tier */*.schema.json`` file this script stores the schema body
to Synapse under the ``org.synapse.classic`` organization, publishing a new
semantic version (MAJOR.MINOR.PATCH). Running this on every merge to ``main``
keeps the registered schemas in lock-step with the repository.

Versioning logic, per schema:
  * Look up the highest existing semantic version in Synapse.
  * If the schema is new, publish ``INITIAL_VERSION`` (default ``1.0.0``).
  * If the body is unchanged from the latest published version, skip it.
  * Otherwise bump the version (patch by default) and publish.

Authentication: a Synapse personal access token is read from the
``SYNAPSE_AUTH_TOKEN`` environment variable (synapseclient picks it up on login).

Environment variables:
  SYNAPSE_AUTH_TOKEN  Synapse PAT used to authenticate (required).
  VERSION_BUMP        Which part to increment: major | minor | patch (default patch).
  INITIAL_VERSION     Version to publish for a brand-new schema (default 1.0.0).
  SCHEMA_GLOB         Override the default glob of schema files (optional).
  DRY_RUN             Truthy value -> store with dry_run=True (nothing persisted).
"""

import asyncio
import glob
import json
import os
import re
import sys

from synapseclient import Synapse
from synapseclient.models import JSONSchema

ORG = "org.synapse.classic"
DEFAULT_GLOB = "model/Tier */*.schema.json"
TRUTHY = {"1", "true", "yes", "on"}
SEMVER_RE = re.compile(r"^\s*v?(\d+)\.(\d+)\.(\d+)\s*$")


def schema_name_from_id(schema_id: str) -> str:
    """Extract the Synapse schema name from a registered ``$id``.

    e.g. ".../registered/org.synapse.classic-tier1-study-identity-discovery"
         -> "tier1-study-identity-discovery"
    """
    marker = f"registered/{ORG}-"
    idx = schema_id.find(marker)
    if idx == -1:
        raise ValueError(
            f"$id '{schema_id}' does not contain the expected "
            f"'registered/{ORG}-' prefix"
        )
    return schema_id[idx + len(marker):]


def parse_semver(value):
    """Return (major, minor, patch) tuple or None if not a semantic version."""
    if value is None:
        return None
    match = SEMVER_RE.match(str(value))
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def extract_version(info):
    """Pull a semantic version tuple out of a JSONSchemaVersionInfo / dict."""
    for attr in ("semantic_version", "semanticVersion", "version", "version_number"):
        value = getattr(info, attr, None)
        if value is None and isinstance(info, dict):
            value = info.get(attr)
        parsed = parse_semver(value)
        if parsed:
            return parsed
    return None


def bump(version, part: str):
    major, minor, patch = version
    if part == "major":
        return (major + 1, 0, 0)
    if part == "minor":
        return (major, minor + 1, 0)
    return (major, minor, patch + 1)


def normalize_body(body: dict) -> str:
    """Stable serialization for change detection, ignoring the ``$id`` URI."""
    trimmed = {k: v for k, v in body.items() if k != "$id"}
    return json.dumps(trimmed, sort_keys=True, ensure_ascii=False)


async def latest_published(schema: JSONSchema, syn: Synapse):
    """Return (latest_semver_tuple, latest_body) or (None, None) if schema is new."""
    latest_version = None
    try:
        async for info in schema.get_versions_async(synapse_client=syn):
            parsed = extract_version(info)
            if parsed and (latest_version is None or parsed > latest_version):
                latest_version = parsed
    except Exception:
        # Schema does not exist yet (no versions to list).
        return None, None

    if latest_version is None:
        return None, None

    try:
        body = await schema.get_body_async(synapse_client=syn)
    except Exception:
        body = None
    return latest_version, body


async def register_one(syn, path, bump_part, initial_version, dry_run) -> bool:
    """Publish one schema. Returns True if a new version was stored."""
    with open(path, encoding="utf-8") as fh:
        body = json.load(fh)

    schema_id = body.get("$id")
    if not schema_id:
        raise ValueError(f"{path}: schema is missing a '$id'")
    name = schema_name_from_id(schema_id)
    schema = JSONSchema(organization_name=ORG, name=name)

    latest_version, latest_body = await latest_published(schema, syn)

    if latest_version is None:
        new_version = initial_version
    else:
        if latest_body is not None and normalize_body(latest_body) == normalize_body(body):
            cur = ".".join(map(str, latest_version))
            print(f"unchanged  {ORG}-{name} (latest {cur}) -> skipped")
            return False
        new_version = bump(latest_version, bump_part)

    version_str = ".".join(map(str, new_version))
    await schema.store_async(
        schema_body=body, version=version_str, dry_run=dry_run, synapse_client=syn
    )

    label = "(dry-run) " if dry_run else ""
    print(f"{label}published {ORG}-{name} {version_str}  <- {path}")
    return True


async def main() -> int:
    token = os.environ.get("SYNAPSE_AUTH_TOKEN")
    if not token:
        print("ERROR: SYNAPSE_AUTH_TOKEN is not set", file=sys.stderr)
        return 1

    bump_part = os.environ.get("VERSION_BUMP", "patch").strip().lower()
    if bump_part not in {"major", "minor", "patch"}:
        print(f"ERROR: VERSION_BUMP must be major|minor|patch, got '{bump_part}'", file=sys.stderr)
        return 1

    initial_version = parse_semver(os.environ.get("INITIAL_VERSION", "1.0.0"))
    if initial_version is None:
        print("ERROR: INITIAL_VERSION must be a semantic version (e.g. 1.0.0)", file=sys.stderr)
        return 1

    dry_run = os.environ.get("DRY_RUN", "").lower() in TRUTHY
    pattern = os.environ.get("SCHEMA_GLOB", DEFAULT_GLOB)
    paths = sorted(glob.glob(pattern))
    if not paths:
        print(f"ERROR: no schema files matched '{pattern}'", file=sys.stderr)
        return 1

    syn = Synapse()
    syn.login(authToken=token)

    published = 0
    failures = []
    for path in paths:
        try:
            if await register_one(syn, path, bump_part, initial_version, dry_run):
                published += 1
        except Exception as exc:  # noqa: BLE001 - report per-file, keep going
            print(f"FAILED {path}: {exc}", file=sys.stderr)
            failures.append(path)

    if failures:
        print(f"\n{len(failures)} of {len(paths)} schema(s) failed", file=sys.stderr)
        return 1

    print(f"\nDone: {published} new version(s) published, "
          f"{len(paths) - published} unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
