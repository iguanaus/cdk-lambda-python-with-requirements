# CDK-Lambda-Python-With-Requirements

Project template to show how to use CDK to create a basic lambda function with some pip/python requirements.

## Deployment Instructions

1. `docker run --rm --volume=$(pwd):/lambda-build -w=/lambda-build lambci/lambda:build-python3.8 pip install -r requirements-layer.txt --target build/python`
2. `cdk synth`
3. `cdk deploy`

## Testing

Go to the AWS console and hit `test`!
