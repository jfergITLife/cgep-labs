# CGEP Labs

Hands-on GRC engineering exercises using Terraform, AWS, and machine-readable evidence.

## Layout

- `terraform/primitives/`: independently deployed lab resources.
- `terraform/modules/`: future reusable modules.
- `scripts/`: evidence processing utilities.
- `evidence/lab-2-3/`: reviewed, sanitized evidence for Lab 2.3.

## Lab 2.3

The compliant S3 primitive deploys a data bucket and a separate access-log destination. See [the lab README](terraform/primitives/compliant-s3/README.md) for controls and limitations, and [the evidence notes](evidence/lab-2-3/README.md) for provenance and cleanup status.

Course source: [GRCEngClub/cgep-labs](https://github.com/GRCEngClub/cgep-labs). This is the student's own portfolio repository, not the upstream course repository.

Lab 2.3 completed: configuration verified, sanitized evidence published, and live lab resources removed. Root access, IAM lab access and billing alerts are retained for future labs.
