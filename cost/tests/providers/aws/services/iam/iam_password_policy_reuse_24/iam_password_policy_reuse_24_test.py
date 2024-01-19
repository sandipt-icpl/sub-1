from unittest import mock

from boto3 import client
from moto import mock_iam

from tests.providers.aws.audit_info_utils import (
    AWS_ACCOUNT_ARN,
    AWS_ACCOUNT_NUMBER,
    AWS_REGION_US_EAST_1,
    set_mocked_aws_audit_info,
)


class Test_iam_password_policy_reuse_24:
    from tests.providers.aws.audit_info_utils import (
        AWS_ACCOUNT_ARN,
        AWS_ACCOUNT_NUMBER,
        AWS_REGION_US_EAST_1,
        set_mocked_aws_audit_info,
    )

    @mock_iam
    def test_iam_password_policy_reuse_prevention_equal_24(self):
        iam_client = client("iam")
        # update password policy
        iam_client.update_account_password_policy(PasswordReusePrevention=24)

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_US_EAST_1])
        from prowler.providers.aws.services.iam.iam_service import IAM

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.iam.iam_password_policy_reuse_24.iam_password_policy_reuse_24.iam_client",
            new=IAM(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.iam.iam_password_policy_reuse_24.iam_password_policy_reuse_24 import (
                iam_password_policy_reuse_24,
            )

            check = iam_password_policy_reuse_24()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == "IAM password policy reuse prevention is equal to 24."
            )
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER
            assert result[0].resource_arn == AWS_ACCOUNT_ARN
            assert result[0].region == AWS_REGION_US_EAST_1

    @mock_iam
    def test_iam_password_policy_reuse_prevention_less_24(self):
        iam_client = client("iam")
        # update password policy
        iam_client.update_account_password_policy(PasswordReusePrevention=20)

        current_audit_info = set_mocked_aws_audit_info([AWS_REGION_US_EAST_1])
        from prowler.providers.aws.services.iam.iam_service import IAM

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.iam.iam_password_policy_reuse_24.iam_password_policy_reuse_24.iam_client",
            new=IAM(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.iam.iam_password_policy_reuse_24.iam_password_policy_reuse_24 import (
                iam_password_policy_reuse_24,
            )

            check = iam_password_policy_reuse_24()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "IAM password policy reuse prevention is less than 24 or not set."
            )
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER
            assert result[0].resource_arn == AWS_ACCOUNT_ARN
            assert result[0].region == AWS_REGION_US_EAST_1
