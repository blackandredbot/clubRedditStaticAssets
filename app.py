#!/usr/bin/env python3
import os

import aws_cdk as cdk

from club_reddit_static_assets.club_reddit_static_assets_pipeline_stack import \
    ClubRedditStaticAssetsStack

app = cdk.App()
default_env = cdk.Environment(account="363951782376", region="us-east-1")
application_prefix = "ClubRedditStaticAssets"

ClubRedditStaticAssetsStack(
    app,
    f"{application_prefix}Stack",
    env=default_env,
    application_prefix=application_prefix,
)

app.synth()
