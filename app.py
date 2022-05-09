"""Main entrance for AWS CDK deployment.
Deploys a sample script with python dependencies to lambda.

BEFORE RUNNING THIS, make sure to create the `build` dependency folder. To do this:
docker run --rm --volume=$(pwd):/lambda-build -w=/lambda-build lambci/lambda:build-python3.8 pip install -r requirements-layer.txt --target build/python
"""

from aws_cdk import (
    aws_ec2 as ec2,
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    App, Duration, Environment, Stack
)


# External resources that this app depends on.
AWS_ACCOUNT_ID = '<>'
AWS_REGION = 'eu-west-2'


class LambdaCronStack(Stack):
    def __init__(self, app: App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaLayer = lambda_.LayerVersion(
            self,
            'lambda-layer-dependencies-template',
            code = lambda_.Code.from_asset("build/"),
            compatible_runtimes = [lambda_.Runtime.PYTHON_3_8],
        )

        lambdaFn = lambda_.Function(
            self, "template-lambda",
            code=lambda_.InlineCode(handler_code),
            handler="index.lambda_handler",
            timeout=Duration.seconds(900),
            layers = [lambdaLayer],
            runtime=lambda_.Runtime.PYTHON_3_8,
        )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(Duration.minutes(5)),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))


app = App()
LambdaCronStack(app, "Template-Lambda", env=Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION))
app.synth()
