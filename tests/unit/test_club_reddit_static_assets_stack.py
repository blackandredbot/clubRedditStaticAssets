import aws_cdk as core
import aws_cdk.assertions as assertions

from club_reddit_static_assets.club_reddit_static_assets_pipeline_stack import \
    ClubRedditStaticAssetsStack


# example tests. To run these tests, uncomment this file along with the example
# resource in club_reddit_static_assets/club_reddit_static_assets_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ClubRedditStaticAssetsStack(app, "club-reddit-static-assets")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
