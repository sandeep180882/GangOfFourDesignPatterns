from patterns.creational.abstract_factory.pattern import (
    AwsFactory,
    AzureFactory,
    BlobStorage,
    Deployment,
    S3Storage,
    ServiceBusQueue,
    SqsQueue,
)


def test_factories_produce_consistent_families():
    aws, azure = AwsFactory(), AzureFactory()
    assert isinstance(aws.create_storage(), S3Storage)
    assert isinstance(aws.create_queue(), SqsQueue)
    assert isinstance(azure.create_storage(), BlobStorage)
    assert isinstance(azure.create_queue(), ServiceBusQueue)


def test_client_works_with_either_family():
    aws_steps = Deployment(AwsFactory()).deploy("app")
    azure_steps = Deployment(AzureFactory()).deploy("app")
    assert len(aws_steps) == len(azure_steps) == 3
    assert aws_steps[0].startswith("s3://")
    assert "blob.core.windows.net" in azure_steps[0]
    assert aws_steps != azure_steps
