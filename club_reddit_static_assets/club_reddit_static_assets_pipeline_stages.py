import aws_cdk as cdk
from constructs import Construct

from club_reddit_static_assets.club_reddit_static_assets_lambda_stack import (
    ClubRedditStaticAssetsLambdaStack,
)
from club_reddit_static_assets.club_reddit_static_assets_storage_stack import (
    ClubRedditStaticAssetsStorageStack,
)


class AppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaStack = ClubRedditStaticAssetsLambdaStack(self, "LambdaStack")

        storageStack = ClubRedditStaticAssetsStorageStack(
            self, "StorageStack", assets_bucket=lambdaStack.assets_bucket
        )
