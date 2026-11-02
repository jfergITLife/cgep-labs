import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "private-evidence" / "lab-2-3"
DEST = ROOT / "evidence" / "lab-2-3"

# Only these configuration fields may enter the published evidence.
ALLOWED = {
    "aws_s3_bucket": {"tags", "tags_all"},
    "aws_s3_bucket_server_side_encryption_configuration": {"rule"},
    "aws_s3_bucket_versioning": {"versioning_configuration"},
    "aws_s3_bucket_public_access_block": {
        "block_public_acls",
        "block_public_policy",
        "ignore_public_acls",
        "restrict_public_buckets",
    },
    "aws_s3_bucket_logging": {"target_prefix"},
    "aws_s3_bucket_ownership_controls": {"rule"},
    "aws_s3_bucket_acl": {"acl"},
}

NESTED = {
    "apply_server_side_encryption_by_default",
    "sse_algorithm",
    "bucket_key_enabled",
    "status",
    "mfa_delete",
    "object_ownership",
}

TAGS = {"Project", "Environment", "ManagedBy", "ComplianceScope"}


def clean_nested(value):
    if isinstance(value, dict):
        return {key: clean_nested(item) for key, item in value.items() if key in NESTED}
    if isinstance(value, list):
        return [clean_nested(item) for item in value]
    return value


def extract(source_document, source_section):
    resources = source_document[source_section]["root_module"]["resources"]
    extracted_resources = []

    for resource in resources:
        allowed = ALLOWED.get(resource["type"])
        if allowed is None:
            continue

        values = {}
        for key, value in resource["values"].items():
            if key not in allowed:
                continue
            if key in {"tags", "tags_all"}:
                values[key] = {k: v for k, v in (value or {}).items() if k in TAGS}
            else:
                values[key] = clean_nested(value)

        extracted_resources.append(
            {
                "address": resource["address"],
                "type": resource["type"],
                "name": resource["name"],
                "values": values,
            }
        )

    return {
        "evidence_kind": "sanitized_configuration_extract",
        "source_section": source_section,
        "deployment_phase": "post-deployment, after tag corrections",
        "limitations": [
            "Not a complete Terraform plan or state export.",
            "Identifiers, outputs, and unselected fields are omitted.",
            "Does not prove actual access-log delivery or audit review.",
        ],
        "resources": extracted_resources,
    }


DEST.mkdir(parents=True, exist_ok=True)

for name, section in [("plan", "planned_values"), ("state", "values")]:
    source = SOURCE / f"{name}.raw.json"
    document = json.loads(source.read_text(encoding="utf-8-sig"))
    result = extract(document, section)
    destination = DEST / f"{name}.json"
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Created {destination.name}: {len(result['resources'])} resources")
