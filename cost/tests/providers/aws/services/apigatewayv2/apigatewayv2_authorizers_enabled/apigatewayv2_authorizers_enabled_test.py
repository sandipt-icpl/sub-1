from unittest import mock

import botocore
from boto3 import client
from mock import patch
from moto import mock_apigatewayv2

from tests.providers.aws.audit_info_utils import (
    AWS_REGION_US_EAST_1,
    set_mocked_aws_audit_info,
)

# Mocking ApiGatewayV2 Calls
make_api_call = botocore.client.BaseClient._make_api_call


def mock_make_api_call(self, operation_name, kwarg):
    """
    We have to mock every AWS API call using Boto3

    Rationale -> https://github.com/boto/botocore/blob/develop/botocore/client.py#L810:L816
    """
    if operation_name == "GetAuthorizers":
        return {"Items": [{"AuthorizerId": "authorizer-id", "Name": "test-authorizer"}]}
    elif operation_name == "GetStages":
        return {
            "Items": [
                {
                    "AccessLogSettings": {
                        "DestinationArn": "string",
                        "Format": "string",
                    },
                    "StageName": "test-stage",
                }
            ]
        }
    return make_api_call(self, operation_name, kwarg)


@patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call)
class Test_apigatewayv2_api_authorizers_enabled:
    @mock_apigatewayv2
    def test_apigateway_no_apis(self):
        from prowler.providers.aws.services.apigatewayv2.apigatewayv2_service import (
            ApiGatewayV2,
        )

        current_audit_info = current_audit_info = set_mocked_aws_audit_info(
            [AWS_REGION_US_EAST_1]
        )

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.apigatewayv2.apigatewayv2_api_authorizers_enabled.apigatewayv2_api_authorizers_enabled.apigatewayv2_client",
            new=ApiGatewayV2(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.apigatewayv2.apigatewayv2_api_authorizers_enabled.apigatewayv2_api_authorizers_enabled import (
                apigatewayv2_api_authorizers_enabled,
            )

            check = apigatewayv2_api_authorizers_enabled()
            result = check.execute()

            assert len(result) == 0

    @mock_apigatewayv2
    def test_apigateway_one_api_with_authorizer(self):
        # Create ApiGatewayV2 Mocked Resources
        apigatewayv2_client = client("apigatewayv2", region_name=AWS_REGION_US_EAST_1)
        # Create ApiGatewayV2 API
        api = apigatewayv2_client.create_api(Name="test-api", ProtocolType="HTTP")
        apigatewayv2_client.create_authorizer(
            ApiId=api["ApiId"],
            AuthorizerType="REQUEST",
            IdentitySource=[],
            Name="auth1",
            AuthorizerPayloadFormatVersion="2.0",
        )
        from prowler.providers.aws.services.apigatewayv2.apigatewayv2_service import (
            ApiGatewayV2,
        )

        current_audit_info = current_audit_info = set_mocked_aws_audit_info(
            [AWS_REGION_US_EAST_1]
        )

        with mock.patch(
            "prowler.providers.aws.lib.audit_info.audit_info.current_audit_info",
            new=current_audit_info,
        ), mock.patch(
            "prowler.providers.aws.services.apigatewayv2.apigatewayv2_api_authorizers_enabled.apigatewayv2_api_authorizers_enabled.apigatewayv2_client",
            new=ApiGatewayV2(current_audit_info),
        ):
            # Test Check
            from prowler.providers.aws.services.apigatewayv2.apigatewayv2_api_authorizers_enabled.apigatewayv2_api_authorizers_enabled import (
                apigatewayv2_api_authorizers_enabled,
            )

            check = apigatewayv2_api_authorizers_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"API Gateway V2 test-api ID {api['ApiId']} has an authorizer configured."
            )
            assert result[0].resource_id == "test-api"
            assert (
                result[0].resource_arn
                == f"arn:aws:apigateway:{AWS_REGION_US_EAST_1}::apis/{api['ApiId']}"
            )
            assert result[0].region == AWS_REGION_US_EAST_1
            assert result[0].resource_tags == [{}]
