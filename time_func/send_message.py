from create_bot import bot, scheduler


async def send_scheduled_message(chat_id=-4678304262, bot=bot, message_thread_id=1):
    message = "Здесь сообщение в группу"
    await bot.send_message(chat_id, message, message_thread_id)


async def create_schedule(schedule_time, day_of_week):
        hour = int(schedule_time.split(':')[0])
        minute = int(schedule_time.split(':')[1])
        scheduler.add_job(
            send_scheduled_message,
            'cron', day_of_week=day_of_week, hour=hour, minute=minute)
    