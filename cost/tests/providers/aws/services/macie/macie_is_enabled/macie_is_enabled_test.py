from unittest import mock

from moto import mock_s3

from prowler.providers.aws.services.macie.macie_service import Session
from prowler.providers.aws.services.s3.s3_service import Bucket
from tests.providers.aws.audit_info_utils import (
    AWS_ACCOUNT_NUMBER,
    AWS_REGION_EU_WEST_1,
    set_mocked_aws_audit_info,
)


class Test_macie_is_enabled:
    @mock_s3
    def test_macie_disabled(self):
        s3_client = mock.MagicMock
        s3_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        s3_client.buckets = []
        s3_client.regions_with_buckets = []

        macie_client = mock.MagicMock
        macie_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        macie_client.audited_account = AWS_ACCOUNT_NUMBER
        macie_client.audited_account_arn = f"arn:aws:iam::{AWS_ACCOUNT_NUMBER}:root"
        macie_client.sessions = [
            Session(
                status="DISABLED",
                region="eu-west-1",
            )
        ]
        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.macie_client",
            new=macie_client,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.s3_client",
            new=s3_client,
        ):
            # Test Check
            from prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled import (
                macie_is_enabled,
            )

            check = macie_is_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert result[0].status_extended == "Macie is not enabled."
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER

    @mock_s3
    def test_macie_enabled(self):
        s3_client = mock.MagicMock
        s3_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        s3_client.buckets = []
        s3_client.regions_with_buckets = []

        macie_client = mock.MagicMock
        macie_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        macie_client.audited_account = AWS_ACCOUNT_NUMBER
        macie_client.audited_account_arn = f"arn:aws:iam::{AWS_ACCOUNT_NUMBER}:root"
        macie_client.sessions = [
            Session(
                status="ENABLED",
                region="eu-west-1",
            )
        ]
        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.macie_client",
            new=macie_client,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.s3_client",
            new=s3_client,
        ):
            # Test Check
            from prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled import (
                macie_is_enabled,
            )

            check = macie_is_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert result[0].status_extended == "Macie is enabled."
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER

    @mock_s3
    def test_macie_suspended_ignored(self):
        s3_client = mock.MagicMock
        s3_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        s3_client.buckets = []
        s3_client.regions_with_buckets = []

        macie_client = mock.MagicMock
        macie_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        macie_client.audited_account = AWS_ACCOUNT_NUMBER
        macie_client.audited_account_arn = f"arn:aws:iam::{AWS_ACCOUNT_NUMBER}:root"
        macie_client.sessions = [
            Session(
                status="PAUSED",
                region="eu-west-1",
            )
        ]

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        macie_client.audit_info.ignore_unused_services = True

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.macie_client",
            new=macie_client,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.s3_client",
            new=s3_client,
        ):
            # Test Check
            from prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled import (
                macie_is_enabled,
            )

            check = macie_is_enabled()
            result = check.execute()

            assert len(result) == 0

    @mock_s3
    def test_macie_suspended_ignored_with_buckets(self):
        s3_client = mock.MagicMock
        s3_client.regions_with_buckets = [AWS_REGION_EU_WEST_1]
        s3_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        s3_client.buckets = [
            Bucket(
                name="test",
                arn="test-arn",
                region=AWS_REGION_EU_WEST_1,
            )
        ]

        macie_client = mock.MagicMock
        macie_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        macie_client.audited_account = AWS_ACCOUNT_NUMBER
        macie_client.audited_account_arn = f"arn:aws:iam::{AWS_ACCOUNT_NUMBER}:root"
        macie_client.sessions = [
            Session(
                status="PAUSED",
                region=AWS_REGION_EU_WEST_1,
            )
        ]

        macie_client.audit_info.ignore_unused_services = True
        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.macie_client",
            new=macie_client,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.s3_client",
            new=s3_client,
        ):
            # Test Check
            from prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled import (
                macie_is_enabled,
            )

            check = macie_is_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended == "Macie is currently in a SUSPENDED state."
            )
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER

    @mock_s3
    def test_macie_suspended(self):
        s3_client = mock.MagicMock
        s3_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])

        macie_client = mock.MagicMock
        macie_client.audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])
        macie_client.audited_account = AWS_ACCOUNT_NUMBER
        macie_client.audited_account_arn = f"arn:aws:iam::{AWS_ACCOUNT_NUMBER}:root"
        macie_client.sessions = [
            Session(
                status="PAUSED",
                region="eu-west-1",
            )
        ]
        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.macie_client",
            new=macie_client,
        ), mock.patch(
            "prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled.s3_client",
            new=s3_client,
        ):
            # Test Check
            from prowler.providers.aws.services.macie.macie_is_enabled.macie_is_enabled import (
                macie_is_enabled,
            )

            check = macie_is_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended == "Macie is currently in a SUSPENDED state."
            )
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER
