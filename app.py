import time
import asyncio
import schedule
from taskes import collect_telegram_data_by_chanel_db
from taskes import collect_tokenmetric_day_questions_res_tokenAidb
from taskes import collect_sentiments_data_Tokenmetrics_to_db
from taskes import genrat_sentiments_data_Tokenmetrics_to_db
from taskes import generate_telegram_data_db
from taskes import send_telegram_messages_from_db
from taskes import send_teleg_mesg_from_coinmatric_sementim_db
# "@trending"
# Define the asynchronous task function
async def job_15_min():
    # print("Running the scheduled job: collect_telegram_data")
    # await collect_telegram_data_by_chanel_db("@trending")
    # generate_telegram_data_db()
    # await send_telegram_messages_from_db()
    # use 3 function collect--gen--send foreach chanel
    # await asyncio.sleep(60)
    # await collect_telegram_data_by_chanel_db("@TrendingHot_botsol")
    # generate_telegram_data_db()
    # await send_telegram_messages_from_db()
    # # testing-->
    collect_sentiments_data_Tokenmetrics_to_db()
    genrat_sentiments_data_Tokenmetrics_to_db()
    await send_teleg_mesg_from_coinmatric_sementim_db()


async def job_20_min():
    collect_sentiments_data_Tokenmetrics_to_db()





# Define a wrapper to run the asynchronous job in an event loop
def run_async_job_15_min():
    asyncio.create_task(job_15_min())

# Schedule the job to run every 15 minutes
schedule.every(1).minutes.do(run_async_job_15_min)

# Function to run pending tasks
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)





# Display current schedule (for demonstration purposes)
def display_schedule():
    for job in schedule.jobs:
        print(f"Task: {job.job_func.__name__}, Schedule: {job}")

print("Current Schedule:")
display_schedule()

# Start the scheduler
if __name__ == "__main__":
    asyncio.run(run_schedule())
