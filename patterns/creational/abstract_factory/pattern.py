"""Abstract Factory: matching Storage + Queue + Compute families for AWS and Azure."""
from __future__ import annotations

from abc import ABC, abstractmethod


# --- Abstract products -------------------------------------------------------
class Storage(ABC):
    @abstractmethod
    def upload(self, name: str) -> str: ...


class Queue(ABC):
    @abstractmethod
    def publish(self, message: str) -> str: ...


class Compute(ABC):
    @abstractmethod
    def launch(self, image: str) -> str: ...


# --- AWS family --------------------------------------------------------------
class S3Storage(Storage):
    def upload(self, name: str) -> str:
        return f"s3://bucket/{name}"


class SqsQueue(Queue):
    def publish(self, message: str) -> str:
        return f"SQS <- {message}"


class Ec2Compute(Compute):
    def launch(self, image: str) -> str:
        return f"EC2 instance running {image}"


# --- Azure family ------------------------------------------------------------
class BlobStorage(Storage):
    def upload(self, name: str) -> str:
        return f"https://account.blob.core.windows.net/container/{name}"


class ServiceBusQueue(Queue):
    def publish(self, message: str) -> str:
        return f"ServiceBus <- {message}"


class AzureVmCompute(Compute):
    def launch(self, image: str) -> str:
        return f"Azure VM running {image}"


# --- Abstract factory and concrete factories ---------------------------------
class CloudFactory(ABC):
    """Abstract factory: creates a consistent family of related products."""

    @abstractmethod
    def create_storage(self) -> Storage: ...

    @abstractmethod
    def create_queue(self) -> Queue: ...

    @abstractmethod
    def create_compute(self) -> Compute: ...


class AwsFactory(CloudFactory):
    def create_storage(self) -> Storage:
        return S3Storage()

    def create_queue(self) -> Queue:
        return SqsQueue()

    def create_compute(self) -> Compute:
        return Ec2Compute()


class AzureFactory(CloudFactory):
    def create_storage(self) -> Storage:
        return BlobStorage()

    def create_queue(self) -> Queue:
        return ServiceBusQueue()

    def create_compute(self) -> Compute:
        return AzureVmCompute()


class Deployment:
    """Client: depends only on abstractions, so the provider is swappable."""

    def __init__(self, cloud: CloudFactory) -> None:
        self.storage = cloud.create_storage()
        self.queue = cloud.create_queue()
        self.compute = cloud.create_compute()

    def deploy(self, app: str) -> list[str]:
        return [
            self.storage.upload(f"{app}.zip"),
            self.compute.launch(app),
            self.queue.publish(f"{app} deployed"),
        ]
