# Lab 2.3: First compliant S3 resource

This primitive implements safeguards supporting NIST SP 800-53 SC-28 (SSE-S3/AES256 encryption on both buckets), AC-3 (four public-access block settings on both buckets), CM-6 (four required tags and primary-bucket versioning), and AU-3/AU-6 (server access logging to a separate bucket available for review). These safeguards are a lab baseline, not evidence of complete organizational compliance; storing logs does not itself establish an audit-review process.

## Configuration

- Region: `us-east-1`; project: `cgep-lab`; environment: `dev`.
- Terraform >=1.6; provider constraints match the guide: AWS ~>5.0, random ~>3.6.
- Validated with Terraform 1.16.4, AWS provider 5.100.0, and random 3.9.1.
- Eleven managed resources including the local random suffix.
- This implementation follows the guide's `BucketOwnerPreferred` and `log-delivery-write` ACL approach. The logging resource explicitly depends on the ACL to avoid configuring logging before destination permissions exist.
- The log bucket is encrypted and public-blocked, but is not versioned. The guide's prose claims both buckets are versioned; its code only enables primary-bucket versioning.
- AWS recommends a bucket policy for new log-delivery configurations; the ACL method is retained here to follow the exercise.

## Authentication and execution

In Git Bash, authenticate using `aws login --profile cgep-labs`. The separate `cgep-terraform` profile uses `credential_process` to retrieve temporary credentials from that login. Set `export AWS_PROFILE=cgep-terraform` and verify the identity before planning. Never put credentials in Terraform or commit them.

Run `terraform init`, `terraform fmt -check`, `terraform validate`, then `terraform plan -out=tfplan -var="project_name=cgep-lab" -var="environment=dev"`. Review the account, region and all changes before applying the saved plan. Plans and state remain private.

## Evidence and guide corrections

Published plan/state files are explicitly labeled sanitized configuration extracts, not full Terraform JSON exports. The plan was captured after deployment and tag corrections, with no changes required. Raw exports remain in ignored `private-evidence/`; future course policies expecting native Terraform JSON must use those private exports or adapt to the extract schema.

Terraform state JSON can contain secrets even when named `state.json`. Renaming/exporting state does not make it public-safe. The sanitization script selects only known configuration fields; published files are also reviewed before committing.

Tag keys are case-sensitive. `project` and `ComplianceScpe` were corrected to `Project` and `ComplianceScope`, applied, and independently verified. The dependency lock is ignored to match this course's submission instructions, although HashiCorp normally recommends committing it.

Cleanup must handle object versions and delete markers, not only current objects. Evidence is pushed and verified before teardown. The destroy plan must contain only this lab's resources.

## References

- https://github.com/GRCEngClub/cgep-labs/blob/main/guides/02_03_first_compliant_resource.md
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-server-access-logging.html
- https://developer.hashicorp.com/terraform/cli/commands/show
- https://developer.hashicorp.com/terraform/language/files/dependency-lock
