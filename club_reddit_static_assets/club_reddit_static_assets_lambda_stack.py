from aws_cdk import Duration, RemovalPolicy, Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3d
from aws_solutions_constructs.aws_lambda_s3 import LambdaToS3
from constructs import Construct


class ClubRedditStaticAssetsLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        static_assets_lambda = LambdaToS3(
            self,
            "StaticAssets",
            lambda_function_props=_lambda.FunctionProps(
                code=_lambda.Code.from_asset("lambda"),
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler="update_static_assets.handler",
            ),
        )

        self.assets_bucket = static_assets_lambda.s3_bucket

        # club_reddit_calendar_manager_layer = _lambda.LayerVersion(
        #     self,
        #     "ClubRedditLambdaLayer",
        #     removal_policy=RemovalPolicy.RETAIN,
        #     code=_lambda.Code.from_asset(
        #         "lambda/club_reddit_calendar_manager_layer.zip"
        #     ),
        #     compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
        # )
        #
        # # The code that defines your stack goes here
        # calendar_function = EventbridgeToLambda(
        #     self,
        #     "update_calendar",
        #     lambda_function_props=_lambda.FunctionProps(
        #         code=_lambda.Code.from_asset("lambda"),
        #         runtime=_lambda.Runtime.PYTHON_3_9,
        #         handler="update_calendar.handler",
        #         layers=[club_reddit_calendar_manager_layer],
        #         timeout=Duration.minutes(1),
        #     ),
        #     event_rule_props=events.RuleProps(
        #         schedule=events.Schedule.rate(Duration.hours(18))
        #     ),
        # )
        #
        # calendar_function.lambda_function.role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess")
        # )
