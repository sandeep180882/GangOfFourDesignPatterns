from patterns.creational.abstract_factory.pattern import AwsFactory, AzureFactory, Deployment


def run() -> None:
    print("=== Abstract Factory: Cross-Cloud Infrastructure ===")
    for name, factory in (("AWS", AwsFactory()), ("Azure", AzureFactory())):
        print(f"--- Deploying 'orders-api' on {name} ---")
        for step in Deployment(factory).deploy("orders-api"):
            print(f"  {step}")


if __name__ == "__main__":
    run()
