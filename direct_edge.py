from agent_framework import (
    Executor,
    WorkflowContext,
    WorkflowBuilder,
    handler,
    executor
)

import asyncio

class UpperCase(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        await ctx.send_message(text.upper())


@executor(id='remove_vowels')
async def remove_vowels(text: str, ctx:WorkflowContext[str, str]) -> None:
    await ctx.yield_output(''.join([c for c in text if c not in 'AEIOU']))



async def main():
    upper = UpperCase(id='uppercase')
    builder = WorkflowBuilder()
    builder.add_edge(upper, remove_vowels)
    builder.set_start_executor(upper)
    workflow = builder.build()
    events = await workflow.run('hola mundo')
    print(events.get_outputs())

if __name__ == "__main__":
    asyncio.run(main())