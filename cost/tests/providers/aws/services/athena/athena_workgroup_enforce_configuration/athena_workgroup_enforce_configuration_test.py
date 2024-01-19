from unittest import mock

from mock import patch
from moto import mock_athena

from tests.providers.aws.audit_info_utils import (
    AWS_ACCOUNT_NUMBER,
    AWS_REGION_EU_WEST_1,
    set_mocked_aws_audit_info,
)
from tests.providers.aws.services.athena.athena_service_test import mock_make_api_call

ATHENA_PRIMARY_WORKGROUP = "primary"
ATHENA_PRIMARY_WORKGROUP_ARN = f"arn:aws:athena:{AWS_REGION_EU_WEST_1}:{AWS_ACCOUNT_NUMBER}:workgroup/{ATHENA_PRIMARY_WORKGROUP}"


class Test_athena_workgroup_enforce_configuration:
    @mock_athena
    def test_primary_workgroup_configuration_not_enforced(self):
        from prowler.providers.aws.services.athena.athena_service import Athena

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.athena.athena_workgroup_enforce_configuration.athena_workgroup_enforce_configuration.athena_client",
            new=Athena(current_audit_info),
        ):
            from prowler.providers.aws.services.athena.athena_workgroup_enforce_configuration.athena_workgroup_enforce_configuration import (
                athena_workgroup_enforce_configuration,
            )

            check = athena_workgroup_enforce_configuration()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"Athena WorkGroup {ATHENA_PRIMARY_WORKGROUP} does not enforce the workgroup configuration, so it can be overridden by the client-side settings."
            )
            assert result[0].resource_id == ATHENA_PRIMARY_WORKGROUP
            assert result[0].resource_arn == ATHENA_PRIMARY_WORKGROUP_ARN
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_tags == []

    @mock_athena
    def test_primary_workgroup_configuration_not_enforced_ignoring(self):
        from prowler.providers.aws.services.athena.athena_service import Athena

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        current_audit_info.ignore_unused_services = True

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.athena.athena_workgroup_enforce_configuration.athena_workgroup_enforce_configuration.athena_client",
            new=Athena(current_audit_info),
        ):
            from prowler.providers.aws.services.athena.athena_workgroup_enforce_configuration.athena_workgroup_enforce_configuration import (
                athena_workgroup_enforce_configuration,
            )

            check = athena_workgroup_enforce_configuration()
            result = check.execute()

            assert len(result) == 0

    @mock_athena
    # We mock the get_work_group to return a workgroup not enforcing configuration
    @patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call)
    def test_primary_workgroup_configuration_enforced(self):
        from prowler.providers.aws.services.athena.athena_service import Athena

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.athena.athena_workgroup_enforce_configuration.athena_workgroup_enforce_configuration.athena_client",
            new=Athena(current_audit_info),
        ):
            from prowler.providers.aws.services.athena.athena_workgroup_enforce_configuration.athena_workgroup_enforce_configuration import (
                athena_workgroup_enforce_configuration,
            )

            check = athena_workgroup_enforce_configuration()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"Athena WorkGroup {ATHENA_PRIMARY_WORKGROUP} enforces the workgroup configuration, so it cannot be overridden by the client-side settings."
            )
            assert result[0].resource_id == ATHENA_PRIMARY_WORKGROUP
            assert result[0].resource_arn == ATHENA_PRIMARY_WORKGROUP_ARN
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_tags == []
