from typing import Never
from agent_framework import (
    WorkflowBuilder,
    WorkflowContext,
    executor,
)
import asyncio



@executor
async def dispatcher(work_message: str, ctx: WorkflowContext[str]) -> None:
    await ctx.send_message(work_message)


@executor(id="summarizer")
async def summarizer(work_message: str, ctx: WorkflowContext[str]) -> None:
    await ctx.send_message(f'worker 1 summarized: {work_message}')


@executor(id="sentiment_detector")
async def sentiment_detector(work_message: str, ctx: WorkflowContext[str]) -> None:
    await ctx.send_message(f'worker 2 detected sentiment: {work_message}')  


@executor(id="keyword_finder")
async def keyword_finder(work_message: str, ctx: WorkflowContext[str]) -> None:
    await ctx.send_message(f'worker 3 found keywords: {work_message}')  

@executor(id='aggregator')
async def aggregator(work_message: list[str], ctx: WorkflowContext[Never, list[str]]) -> None:
    await ctx.yield_output(work_message)


async def main():

    builder = WorkflowBuilder()
    builder.set_start_executor(dispatcher)
    builder.add_fan_out_edges(dispatcher, [summarizer, sentiment_detector, keyword_finder])
    builder.add_fan_in_edges([summarizer, sentiment_detector, keyword_finder], aggregator)
    workflow = builder.build()
    events = await workflow.run('data to work with')
    print(events.get_outputs())


if __name__ == "__main__":
    asyncio.run(main())
