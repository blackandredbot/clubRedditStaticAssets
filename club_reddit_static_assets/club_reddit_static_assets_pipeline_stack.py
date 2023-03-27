from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct

from club_reddit_static_assets.club_reddit_static_assets_pipeline_stages import \
    AppStage


class ClubRedditStaticAssetsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # CI/CD Integration using CDK Pipelines
        pipeline = CodePipeline(
            self,
            "Pipeline",
            pipeline_name="StaticAssets",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    "blackandredbot/clubRedditStaticAssets", "mainline"
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python3 -m pip install -r lambda/update_static_assets_reqs.txt -t ./lambda",
                    "zip -r lambda/club_reddit_static_assets_layer.zip ./lambda/",
                    "python -m pip install -r requirements.txt",
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(AppStage(self, "ApplicationStage"))
