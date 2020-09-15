from aws_cdk import core
import aws_cdk.aws_dynamodb as ddb
import aws_cdk.aws_lambda as lamb
import aws_cdk.aws_apigateway as gateway
import aws_cdk.aws_cognito as cognito

import os
# Scrabble folder (parent of stack folder)
dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
path = os.path.join(dirname, 'src')
print(path)

class StackStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Database resources
        # TODO: Add AWS RDS Postgresql db

        user_pool = cognito.UserPool(self, 'UserPool', )

        game_handler = lamb.Function(self, 'GameHandler',
            runtime=lamb.Runtime.PYTHON_3_7,
            handler='index.handler',
            code = lamb.Code.from_asset(path),
            )
        game_handler_integration = gateway.LambdaIntegration(game_handler, proxy=False)

        default_cors = gateway.CorsOptions(allow_origins=['http://localhost:3000'], allow_headers=['Authorization'])
        game_api = gateway.LambdaRestApi(self,
                        'GameApi',
                        handler=game_handler,
                        proxy=False,
                        default_cors_preflight_options=default_cors,
                        )
        play = game_api.root.add_resource('play')
        play.add_method('GET', game_handler_integration)
        # play.add_method('POST', game_handler_integration)
