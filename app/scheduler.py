import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from  telegram_bot.publisher import publish_to_channel
from graph.workflow import workflow

async def scheduler_job(application):
    result = await asyncio.to_thread(workflow.invoke, {"topic": "", "iteration": 0})
    await publish_to_channel(application, result["formatted_content"])

def start_scheduler(application):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduler_job, 
                      trigger="cron",
                      hour=21,
                      minute=0,
                      timezone="Asia/Kolkata",
                      args=[application],
                      max_instances=1,
                      coalesce=True,
                      misfire_grace_time=3600
                    )  # Adjust the interval as needed
    scheduler.start()

