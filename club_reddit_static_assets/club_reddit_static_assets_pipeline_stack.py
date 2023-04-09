from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct

from club_reddit_static_assets.club_reddit_static_assets_pipeline_stages import AppStage


class ClubRedditStaticAssetsStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, application_prefix: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # CI/CD Integration using CDK Pipelines
        pipeline = CodePipeline(
            self,
            "Pipeline",
            pipeline_name=f"{application_prefix}Pipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    "blackandredbot/clubRedditStaticAssets", "mainline"
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python3 -m pip install -r lambdas/update_assets/update_static_assets_reqs.txt -t ./lambdas/update_assets/",
                    "zip -r lambdas/update_assets/club_reddit_static_assets_layer.zip ./lambdas/update_assets",
                    "python -m pip install -r requirements.txt",
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(AppStage(self, f"{application_prefix}AppStage"))
