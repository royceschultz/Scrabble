#!/usr/bin/env python3

from aws_cdk import core

from stack.stack_stack import StackStack


app = core.App()
StackStack(app, "stack")

app.synth()
