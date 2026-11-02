# Lab 2.3 evidence

- `plan.json`: sanitized extract from a post-deployment, post-correction no-change plan. It is not pre-deployment evidence.
- `state.json`: sanitized extract of the deployed configuration before cleanup.
- `aws-verification.json`: independent AWS API checks, with account/bucket identifiers excluded.
- `manifest.json`: SHA-256 hashes of the published evidence files. Hashes detect changes relative to this manifest; they are not a signature or proof of origin.
- `cleanup.json`: added after teardown is independently verified.

The configuration was checked for encryption, public-access blocks, tags, primary versioning, log target/prefix, log ownership and log-delivery group permissions. See the verification JSON for observations and collection time. Any observed log objects indicate delivery occurred, not that every request was captured or reviewed.

Identifiers, outputs and unselected attributes are omitted from the public plan/state extracts. They have a custom `resources` structure and are not drop-in inputs for later policies expecting native Terraform plan/state schemas. Private originals are excluded from Git.

Final status: deployment verified and evidence pushed before teardown. Logging was disabled first, then the remaining 10 managed resources were destroyed. Both buckets were independently confirmed absent from AWS. See `cleanup.json`. No log objects were present during the initial verification; one object under access-logs/ was observed and removed during cleanup. Its record contents were not reviewed, so request coverage and audit review are not established.
