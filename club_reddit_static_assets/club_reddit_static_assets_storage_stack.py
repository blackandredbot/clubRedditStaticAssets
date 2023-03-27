from aws_cdk import Duration, RemovalPolicy, Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_solutions_constructs.aws_lambda_s3 import LambdaToS3
from constructs import Construct


class ClubRedditStaticAssetsStorageStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        deployment = s3deploy.BucketDeployment(self, "DeployStaticAssets",
                                               sources=[s3deploy.Source.asset('assets')],
                                               destination_bucket=assets_bucket
                                               )

