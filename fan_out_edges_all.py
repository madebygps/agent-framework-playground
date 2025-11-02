from typing import Never
from agent_framework import (
    WorkflowBuilder,
    WorkflowContext,
    executor,
)
import asyncio



@executor
async def splitter_executor(work_message: str, ctx: WorkflowContext[str]) -> None:
    await ctx.send_message(work_message)


@executor(id="summarizer")
async def summarizer(work_message: str, ctx: WorkflowContext[Never, str]) -> None:
    await ctx.yield_output(f'worker 1 summarized: {work_message}')


@executor(id="sentiment_detector")
async def sentiment_detector(work_message: str, ctx: WorkflowContext[Never, str]) -> None:
    await ctx.yield_output(f'worker 2 detected sentiment: {work_message}')  


@executor(id="keyword_finder")
async def keyword_finder(work_message: str, ctx: WorkflowContext[Never,str]) -> None:
    await ctx.yield_output(f'worker 3 found keywords: {work_message}')  


async def main():

    builder = WorkflowBuilder()
    builder.set_start_executor(splitter_executor)
    builder.add_fan_out_edges(splitter_executor, [summarizer, sentiment_detector, keyword_finder])
    workflow = builder.build()
    events = await workflow.run('data to work with')
    print(events.get_outputs())


if __name__ == "__main__":
    asyncio.run(main())
