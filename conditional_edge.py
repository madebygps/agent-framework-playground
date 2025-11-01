from agent_framework import (
    WorkflowBuilder,
    WorkflowContext,
    Executor,
    handler,
)

import asyncio

class Email:

    def __init__(self, is_spam: bool, body: str, title: str = ""):
        self.is_spam = is_spam
        self.body = body
        self.title = title


class SpamDetector(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)


    @handler
    async def detect_spam(self, email: Email, ctx: WorkflowContext[Email, str]) -> None:
        spam_keywords = ["buy now", "save big"]
        email.is_spam = any(keyword in email.body.lower() for keyword in spam_keywords)
        await ctx.send_message(email)


class EmailProcessor(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def process_email(self, email: Email, ctx: WorkflowContext[Email, str]) -> None:
        
        
        await ctx.yield_output(f"{email.title} processed successfully.")

class SpamHandler(Executor):
    
    def __init__(self, id: str):
        super().__init__(id=id)
    
    @handler
    async def handle_spam(self, email: Email, ctx: WorkflowContext[Email, str]) -> None:
        
        await ctx.yield_output(f"{email.title} was detected as Spam and handled.")    



async def main():

    spam_detector = SpamDetector(id='spam_detector')
    email_processor = EmailProcessor(id='email_processor')
    spam_handler = SpamHandler(id='spam_handler')

    builder = WorkflowBuilder()
    builder.add_edge(spam_detector, email_processor, condition=lambda e: not e.is_spam)
    builder.add_edge(spam_detector, spam_handler, condition=lambda e: e.is_spam)
    builder.set_start_executor(spam_detector)
    
    workflow = builder.build()
    email = Email(is_spam=False, body="save big", title="hello")
    events = await workflow.run(email)

    print(events.get_outputs())
    print("Final state:", events.get_final_state())

if __name__ == "__main__":
    asyncio.run(main())