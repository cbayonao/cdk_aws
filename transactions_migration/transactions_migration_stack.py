#!/usr/bin/env python3
from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_dms as dms,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct

class TransactionsMigrationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Creación de la tabla de Dynamo
        transactions_table = dynamodb.Table(
            self, "BanescoTransactionsTable",
            table_name="BanescoTransactions",
            partition_key=dynamodb.Attribute(name="pre#id",
                                             type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="transaction_timestamp",
                                        type=dynamodb.AttributeType.STRING),
            read_capacity=2,
            write_capacity=3
        )

        lambda_function_daily_incrementals = _lambda.DockerImageFunction(
            self,
            id="banesco_daily_incrementals",
            function_name="banesco_daily_incrementals",
            code=_lambda.DockerImageCode.from_image_asset(
                directory='lambda_functions/daily_incrementals'
            ),

        )


        daily_rule = events.Rule(
            self,
            id='daily_incrementals_rule',
            schedule=events.Schedule.cron(minute='00', hour='13', day='*', year='*')
        )

        daily_rule.add_target(targets.LambdaFunction(lambda_function_daily_incrementals))

        lambda_function_montly_incrementals = _lambda.DockerImageFunction(
            self,
            id="banesco_montly_incrementals",
            function_name="banesco_montly_incrementals",
            code=_lambda.DockerImageCode.from_image_asset(
                directory='lambda_functions/montly_incrementals'
            )
        )

        montly_rule = events.Rule(
            self,
            id='montly_incrementals_rule',
            schedule=events.Schedule.cron(minute='00', hour='13', day='1', month='*', year='*')
        )

        montly_rule.add_target(targets.LambdaFunction(lambda_function_montly_incrementals))

        transactions_table.grant_write_data(lambda_function_daily_incrementals)
        transactions_table.grant_write_data(lambda_function_montly_incrementals)

        # Crear servicio de Data Migration para mover datos desde SQL Server a DynamoDB
        # dms_replication_instance = dms.CfnReplicationInstance(
        #     self, "BanescoDMSReplicationInstance",
        #     tags='Some tags defined',
        #     replication_instance_identifier="BanescoDMS",
        #     allocated_storage=50,
        #     engine_version="3.4.5",
        #     instance_class="dms.t2.micro",
        #     vpc=None,  # Define tu VPC aquí
        # )


