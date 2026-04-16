"""Basic example: async worker retries."""
import asyncio

async def process(job, tries):
    await asyncio.sleep(0.01)
    return not (job == 'job-2' and tries < 2)

async def main():
    queue = [('job-1', 0), ('job-2', 0), ('job-3', 0)]
    while queue:
        job, tries = queue.pop(0)
        tries += 1
        if await process(job, tries):
            print('done', job, 'tries', tries)
        else:
            print('retry', job, 'tries', tries)
            queue.append((job, tries))

asyncio.run(main())
