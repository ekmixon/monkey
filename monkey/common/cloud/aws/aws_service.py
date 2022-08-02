import logging

import boto3
import botocore

from common.cloud.aws.aws_instance import AwsInstance

INSTANCE_INFORMATION_LIST_KEY = "InstanceInformationList"
INSTANCE_ID_KEY = "InstanceId"
COMPUTER_NAME_KEY = "ComputerName"
PLATFORM_TYPE_KEY = "PlatformType"
IP_ADDRESS_KEY = "IPAddress"

logger = logging.getLogger(__name__)


def filter_instance_data_from_aws_response(response):
    return [
        {
            "instance_id": x[INSTANCE_ID_KEY],
            "name": x[COMPUTER_NAME_KEY],
            "os": x[PLATFORM_TYPE_KEY].lower(),
            "ip_address": x[IP_ADDRESS_KEY],
        }
        for x in response[INSTANCE_INFORMATION_LIST_KEY]
    ]


class AwsService(object):
    """
    A wrapper class around the boto3 client and session modules, which supplies various AWS
    services.

    This class will assume:
        1. That it's running on an EC2 instance
        2. That the instance is associated with the correct IAM role. See
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#iam-role
        for details.
    """

    region = None

    @staticmethod
    def set_region(region):
        AwsService.region = region

    @staticmethod
    def get_client(client_type, region=None):
        return boto3.client(
            client_type, region_name=region if region is not None else AwsService.region
        )

    @staticmethod
    def get_instances():
        """
        Get the information for all instances with the relevant roles.

        This function will assume that it's running on an EC2 instance with the correct IAM role.
        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#iam
        -role for details.

        :raises: botocore.exceptions.ClientError if can't describe local instance information.
        :return: All visible instances from this instance
        """
        current_instance = AwsInstance()
        local_ssm_client = boto3.client("ssm", current_instance.get_region())
        try:
            response = local_ssm_client.describe_instance_information()

            return filter_instance_data_from_aws_response(response)
        except botocore.exceptions.ClientError as e:
            logger.warning(f"AWS client error while trying to get instances: {e}")
            raise e
