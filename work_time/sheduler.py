import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

async def my_task():
    print(f"Текущее время: {datetime.now().strftime('%H:%M:%S')}")
    print("Задача выполнена!")

async def main():
    scheduler = AsyncIOScheduler()

    try:
        while True:
            s = input('Сколько секунд: ')
            try:
                delay = int(s)
                run_date = datetime.now() + timedelta(seconds=delay)
                scheduler.add_job(my_task, 'date', run_date=run_date, id=f'my_task_{delay}')
            except ValueError:
                print(f"Некорректный ввод: '{s}'. Пожалуйста, введите целое число.")
    except KeyboardInterrupt:
        print("\nПрерывание программы.")
    finally:
        await scheduler.shutdown(wait=True)

if __name__ == "__main__":
    asyncio.run(main())
