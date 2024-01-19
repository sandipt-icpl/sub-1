from prowler.lib.check.models import Check, Check_Report_AWS
from prowler.providers.aws.services.cloudtrail.cloudtrail_client import (
    cloudtrail_client,
)
from prowler.providers.aws.services.cloudwatch.cloudwatch_client import (
    cloudwatch_client,
)
from prowler.providers.aws.services.cloudwatch.lib.metric_filters import (
    check_cloudwatch_log_metric_filter,
)
from prowler.providers.aws.services.cloudwatch.logs_client import logs_client


class cloudwatch_changes_to_network_route_tables_alarm_configured(Check):
    def execute(self):
        pattern = r"\$\.eventName\s*=\s*.?CreateRoute.+\$\.eventName\s*=\s*.?CreateRouteTable.+\$\.eventName\s*=\s*.?ReplaceRoute.+\$\.eventName\s*=\s*.?ReplaceRouteTableAssociation.+\$\.eventName\s*=\s*.?DeleteRouteTable.+\$\.eventName\s*=\s*.?DeleteRoute.+\$\.eventName\s*=\s*.?DisassociateRouteTable.?"
        findings = []
        report = Check_Report_AWS(self.metadata())
        report.status = "FAIL"
        report.status_extended = (
            "No CloudWatch log groups found with metric filters or alarms associated."
        )
        report.region = cloudwatch_client.region
        report.resource_id = cloudtrail_client.audited_account
        report.resource_arn = cloudtrail_client.audited_account_arn
        report = check_cloudwatch_log_metric_filter(
            pattern,
            cloudtrail_client.trails,
            logs_client.metric_filters,
            cloudwatch_client.metric_alarms,
            report,
        )

        findings.append(report)
        return findings
