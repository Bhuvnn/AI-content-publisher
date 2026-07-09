import asyncio
from app.logger import get_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram_bot.publisher import publish_to_channel
from graph.workflow import workflow
from agents.topic_generator_agent import topic_generator_agent
from database.crud import save_poem

logger = get_logger(__name__)
scheduler = AsyncIOScheduler()

async def scheduler_job(application):
    topic = await asyncio.to_thread(topic_generator_agent)
    logger.info("Today's topic: %s", topic)
    result = await asyncio.to_thread(workflow.invoke, {"topic": topic, "iteration": 0})
    sent_message = await publish_to_channel(application.bot, result["formatted_content"])
    save_poem(result, sent_message.message_id)


def start_scheduler(application):
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

