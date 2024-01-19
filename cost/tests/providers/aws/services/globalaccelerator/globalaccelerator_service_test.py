import botocore
from mock import patch

from prowler.providers.aws.services.globalaccelerator.globalaccelerator_service import (
    GlobalAccelerator,
)
from tests.providers.aws.audit_info_utils import (
    AWS_ACCOUNT_NUMBER,
    AWS_REGION_US_WEST_2,
    set_mocked_aws_audit_info,
)

# Mocking Access Analyzer Calls
make_api_call = botocore.client.BaseClient._make_api_call

TEST_ACCELERATOR_ARN = f"arn:aws:globalaccelerator::{AWS_ACCOUNT_NUMBER}:accelerator/5555abcd-abcd-5555-abcd-5555EXAMPLE1"


def mock_make_api_call(self, operation_name, kwarg):
    """We have to mock every AWS API call using Boto3"""
    if operation_name == "ListAccelerators":
        return {
            "Accelerators": [
                {
                    "AcceleratorArn": TEST_ACCELERATOR_ARN,
                    "Name": "TestAccelerator",
                    "IpAddressType": "IPV4",
                    "Enabled": True,
                    "IpSets": [
                        {
                            "IpFamily": "IPv4",
                            "IpAddresses": ["192.0.2.250", "198.51.100.52"],
                        }
                    ],
                    "DnsName": "5a5a5a5a5a5a5a5a.awsglobalaccelerator.com",
                    "Status": "DEPLOYED",
                    "CreatedTime": 1552424416.0,
                    "LastModifiedTime": 1569375641.0,
                }
            ]
        }
    if operation_name == "GetSubscriptionState":
        return {"SubscriptionState": "ACTIVE"}

    return make_api_call(self, operation_name, kwarg)


# Patch every AWS call using Boto3 and generate_regional_clients to have 1 client
@patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call)
class Test_GlobalAccelerator_Service:
    # Test GlobalAccelerator Service
    def test_service(self):
        # GlobalAccelerator client for this test class
        audit_info = set_mocked_aws_audit_info()
        globalaccelerator = GlobalAccelerator(audit_info)
        assert globalaccelerator.service == "globalaccelerator"

    # Test GlobalAccelerator Client
    def test_client(self):
        # GlobalAccelerator client for this test class
        audit_info = set_mocked_aws_audit_info()
        globalaccelerator = GlobalAccelerator(audit_info)
        assert globalaccelerator.client.__class__.__name__ == "GlobalAccelerator"

    # Test GlobalAccelerator Session
    def test__get_session__(self):
        # GlobalAccelerator client for this test class
        audit_info = set_mocked_aws_audit_info()
        globalaccelerator = GlobalAccelerator(audit_info)
        assert globalaccelerator.session.__class__.__name__ == "Session"

    def test__list_accelerators__(self):
        # GlobalAccelerator client for this test class
        audit_info = set_mocked_aws_audit_info()
        globalaccelerator = GlobalAccelerator(audit_info)

        accelerator_name = "TestAccelerator"

        assert globalaccelerator.accelerators
        assert len(globalaccelerator.accelerators) == 1
        assert globalaccelerator.accelerators[TEST_ACCELERATOR_ARN]
        assert (
            globalaccelerator.accelerators[TEST_ACCELERATOR_ARN].name
            == accelerator_name
        )
        assert (
            globalaccelerator.accelerators[TEST_ACCELERATOR_ARN].arn
            == TEST_ACCELERATOR_ARN
        )
        assert (
            globalaccelerator.accelerators[TEST_ACCELERATOR_ARN].region
            == AWS_REGION_US_WEST_2
        )
        assert globalaccelerator.accelerators[TEST_ACCELERATOR_ARN].enabled
