#!/usr/bin/env python3
from aws_cdk import (
    BundlingOptions,
    Stack,
    aws_apigateway as _apigw,
    aws_lambda as _lambda
)

from constructs import Construct


class ConsumptionLayerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function_fast_api_application = _lambda.Function(
            self,
            runtime=_lambda.Runtime.PYTHON_3_9,
            id="banesco_lambda_function_fast_api_application",
            function_name="banesco_lambda_function_fast_api_application",
            code=_lambda.Code.from_asset('./lambda_functions/fast_api'),
            handler='main.handler',
            environment={
                "FASTAPI_LIFESPAN": "off"
            }
        )

        base_api = _apigw.RestApi(
            self, 
            'ApiGatewayToConsumption',
            rest_api_name='ApiGatewayToConsumption'
        )


        integration = _apigw.LambdaIntegration(lambda_function_fast_api_application, proxy=True)
        base_api.root.add_resource("{proxy+}").add_method("ANY", integration)