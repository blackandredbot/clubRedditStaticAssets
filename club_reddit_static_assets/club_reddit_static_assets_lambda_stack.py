from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_solutions_constructs.aws_lambda_s3 import LambdaToS3
from constructs import Construct


class ClubRedditStaticAssetsLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        update_assets_lambda = LambdaToS3(
            self,
            "StaticAssets",
            lambda_function_props=_lambda.FunctionProps(
                code=_lambda.Code.from_asset("lambdas/update_assets"),
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler="update_static_assets.handler",
            ),
        )

        self.assets_bucket = static_assets_lambda.s3_bucket
