from datetime import datetime
from unittest.mock import patch

import botocore

from prowler.providers.aws.services.drs.drs_service import DRS
from tests.providers.aws.audit_info_utils import (
    AWS_REGION_US_EAST_1,
    set_mocked_aws_audit_info,
)

# Mocking Calls
make_api_call = botocore.client.BaseClient._make_api_call


def mock_make_api_call(self, operation_name, kwargs):
    """We have to mock every AWS API call using Boto3"""
    if operation_name == "DescribeJobs":
        return {
            "items": [
                {
                    "arn": "arn:aws:disaster-recovery:us-east-1:123456789012:job/jobID1",
                    "creationDateTime": datetime(2024, 1, 1),
                    "endDateTime": datetime(2024, 1, 1),
                    "initiatedBy": "START_RECOVERY",
                    "jobID": "jobID1",
                    "participatingServers": [
                        {
                            "launchStatus": "PENDING",
                            "recoveryInstanceID": "i-1234567890abcdef0",
                            "sourceServerID": "i-1234567890abcdef0",
                        },
                    ],
                    "status": "PENDING",
                    "tags": {"test_tag": "test_value"},
                    "type": "LAUNCH",
                },
            ]
        }

    return make_api_call(self, operation_name, kwargs)


def mock_generate_regional_clients(service, audit_info):
    regional_client = audit_info.audit_session.client(
        service, region_name=AWS_REGION_US_EAST_1
    )
    regional_client.region = AWS_REGION_US_EAST_1
    return {AWS_REGION_US_EAST_1: regional_client}


# Patch every AWS call using Boto3 and generate_regional_clients to have 1 client
@patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call)
@patch(
    "prowler.providers.aws.lib.service.service.generate_regional_clients",
    new=mock_generate_regional_clients,
)
class Test_DRS_Service:
    def test__get_client__(self):
        audit_info = set_mocked_aws_audit_info()
        drs = DRS(audit_info)
        assert drs.regional_clients[AWS_REGION_US_EAST_1].__class__.__name__ == "drs"

    def test__get_service__(self):
        audit_info = set_mocked_aws_audit_info()
        drs = DRS(audit_info)
        assert drs.service == "drs"

    def test__describe_jobs__(self):
        audit_info = set_mocked_aws_audit_info()
        drs = DRS(audit_info)
        assert len(drs.drs_services) == 1
        assert drs.drs_services[0].id == "DRS"
        assert drs.drs_services[0].region == AWS_REGION_US_EAST_1
        assert drs.drs_services[0].status == "ENABLED"
