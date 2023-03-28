from aws_cdk import Stack
from aws_cdk import aws_s3_deployment as s3deploy
from constructs import Construct


class ClubRedditStaticAssetsStorageStack(Stack):
    def __init__(self, scope: Construct, id: str, assets_bucket=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        deployment = s3deploy.BucketDeployment(
            self,
            "DeployStaticAssets",
            sources=[s3deploy.Source.asset("assets")],
            destination_bucket=assets_bucket,
        )
