import aws_cdk as core
import aws_cdk.assertions as assertions

from transactions_migration.transactions_migration_stack import TransactionsMigrationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in transactions_migration/transactions_migration_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TransactionsMigrationStack(app, "transactions-migration")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
