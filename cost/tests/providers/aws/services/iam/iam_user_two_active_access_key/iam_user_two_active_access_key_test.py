from re import search
from unittest import mock

from boto3 import client
from moto import mock_iam

from tests.providers.aws.audit_info_utils import (
    AWS_REGION_US_EAST_1,
    set_mocked_aws_audit_info,
)

AWS_ACCOUNT_NUMBER = "123456789012"


class Test_iam_user_two_active_access_key:
    from tests.providers.aws.audit_info_utils import (
        AWS_ACCOUNT_ARN,
        AWS_ACCOUNT_NUMBER,
        AWS_REGION_US_EAST_1,
        set_mocked_aws_audit_info,
    )

    @mock_iam
    def test_iam_user_two_active_access_key(self):
        # Create IAM Mocked Resources
        iam_client = client("iam")
        user = "test1"
        user_arn = iam_client.create_user(UserName=user)["User"]["Arn"]
        # Create Access Key 1
        iam_client.create_access_key(UserName=user)
        # Create Access Key 2
        iam_client.create_access_key(UserName=user)

        from prowler.providers.aws.services.iam.iam_service import IAM

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_US_EAST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key.iam_client",
            new=IAM(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key import (
                iam_user_two_active_access_key,
            )

            check = iam_user_two_active_access_key()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert result[0].resource_id == user
            assert result[0].resource_arn == user_arn
            assert search(
                f"User {user} has 2 active access keys.", result[0].status_extended
            )

    @mock_iam
    def test_iam_user_one_active_access_key(self):
        # Create IAM User
        iam_client = client("iam")
        user = "test1"
        user_arn = iam_client.create_user(UserName=user)["User"]["Arn"]
        # Create Access Key 1
        iam_client.create_access_key(UserName=user)

        from prowler.providers.aws.services.iam.iam_service import IAM

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_US_EAST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key.iam_client",
            new=IAM(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key import (
                iam_user_two_active_access_key,
            )

            check = iam_user_two_active_access_key()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert result[0].resource_id == user
            assert result[0].resource_arn == user_arn
            assert search(
                f"User {user} does not have 2 active access keys.",
                result[0].status_extended,
            )

    @mock_iam
    def test_iam_user_without_active_access_key(self):
        # Create IAM User
        iam_client = client("iam")
        user = "test1"
        user_arn = iam_client.create_user(UserName=user)["User"]["Arn"]

        from prowler.providers.aws.services.iam.iam_service import IAM

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_US_EAST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key.iam_client",
            new=IAM(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key import (
                iam_user_two_active_access_key,
            )

            check = iam_user_two_active_access_key()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert result[0].resource_id == user
            assert result[0].resource_arn == user_arn
            assert search(
                f"User {user} does not have 2 active access keys.",
                result[0].status_extended,
            )

    @mock_iam
    def test_iam_no_users(self):
        from prowler.providers.aws.services.iam.iam_service import IAM

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_US_EAST_1])

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key.iam_client",
            new=IAM(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.iam.iam_user_two_active_access_key.iam_user_two_active_access_key import (
                iam_user_two_active_access_key,
            )

            check = iam_user_two_active_access_key()
            result = check.execute()

            assert len(result) == 0
