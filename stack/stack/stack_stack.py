from aws_cdk import core
import aws_cdk.aws_dynamodb as ddb
import aws_cdk.aws_lambda as lamb

import os
# Scrabble folder (parent of stack folder)
dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
path = os.path.join(dirname, 'src')
print(path)

class StackStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        dictionary = ddb.Table(self, "Dictionary",
            partition_key=ddb.Attribute(name="word", type=ddb.AttributeType.STRING)
        )


        game_handler = lamb.Function(self, 'GameHandler',
            runtime=lamb.Runtime.PYTHON_3_8,
            handler='index.handler',

            code = lamb.Code.from_asset(path),
            )
