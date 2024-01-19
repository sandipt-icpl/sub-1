# Custom Checks Metadata

In certain organizations, the severity of specific checks might differ from the default values defined in the check's metadata. For instance, while `s3_bucket_level_public_access_block` could be deemed `critical` for some organizations, others might assign a different severity level.

The custom metadata option offers a means to override default metadata set by Prowler

You can utilize `--custom-checks-metadata-file` followed by the path to your custom checks metadata YAML file.

## Available Fields

The list of supported check's metadata fields that can be override are listed as follows:

- Severity

## File Syntax

This feature is available for all the providers supported in Prowler since the metadata format is common between all the providers. The following is the YAML format for the custom checks metadata file:
```yaml title="custom_checks_metadata.yaml"
CustomChecksMetadata:
  aws:
    Checks:
      s3_bucket_level_public_access_block:
        Severity: high
      s3_bucket_no_mfa_delete:
        Severity: high
  azure:
    Checks:
      storage_infrastructure_encryption_is_enabled:
        Severity: medium
  gcp:
    Checks:
      compute_instance_public_ip:
        Severity: critical
```

## Usage

Executing the following command will assess all checks and generate a report while overriding the metadata for those checks:
```sh
prowler <provider> --custom-checks-metadata-file <path/to/custom/metadata>
```

This customization feature enables organizations to tailor the severity of specific checks based on their unique requirements, providing greater flexibility in security assessment and reporting.
