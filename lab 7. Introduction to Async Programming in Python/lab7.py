import asyncio
import aiofiles
import aiohttp
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger1 = logging.getLogger('Задание 1')
logger2 = logging.getLogger('Задание 2')
logger3 = logging.getLogger('Задание 3')
logger45 = logging.getLogger('Задание 4, 5')
logger_main = logging.getLogger('main')

async def read_file_async(filename: str) -> str:
    try:
        async with aiofiles.open(filename, mode='r', encoding='utf-8') as file:
            content = await file.read()
            logger1.info(f"Файл '{filename}' успешно прочитан")
            return content
    except FileNotFoundError:
        logger1.error(f"Файл '{filename}' не найден")
        return ""
    except Exception as e:
        logger1.error(f"Ошибка при чтении файла '{filename}': {e}")
        return ""


async def process_data_async(data: list[int]) -> dict:
    logger2.info(f"Начало обработки данных")
    await asyncio.sleep(0.5)

    if not data:
        raise ValueError("Данные не могут быть пустыми")
    result = {
        "sum": sum(data),
        "avg": sum(data) / len(data),
        "min": min(data),
        "max": max(data),
        "count": len(data)
    }

    return result


async def greet(name: str) -> str:
    logger3.info(f"Начало приветствия для {name}...")
    await asyncio.sleep(2)
    greeting = f"Привет, {name}!"
    logger3.info(greeting)
    return greeting


async def multiple_greetings():
    names = []
    print("Введите имена для приветствия. Для завершение введите and\n")
    while True:
        name = input("> ").strip()
        if not name:
            continue
        if name.lower() == "and":
            break
        names.append(name)

    if not names:
        logger3.error("Не введено ни одного имени!")
        return []

    tasks = [greet(name) for name in names]
    results = await asyncio.gather(*tasks)
    logger3.info("Все приветствия завершены!")
    return results



async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    try:
        logger45.info(f"Начало запроса к: {url}")
        async with session.get(url, timeout=20, ssl=False) as response:
            status = response.status
            content = await response.text()

            result = {
                "url": url,
                "status": status,
                "success": 200 <= status < 400,
                "content": content[:200]
            }

            logger45.info(f"Запрос к {url} завершен со статусом {status}")
            return result

    except aiohttp.ClientError as e:
        error_msg = f"Сетевая ошибка: {type(e).__name__}"
        logger45.error(f"Ошибка при запросе к {url}. {error_msg}")
        return {
            "url": url,
            "status": None,
            "content": None,
            "success": False,
            "error": error_msg
        }

    except asyncio.TimeoutError:
        error_msg = "Таймаут запроса (20 секунд)"
        logger45.error(f"Таймаут при запросе к {url}")
        return {
            "url": url,
            "status": None,
            "content": None,
            "success": False,
            "error": error_msg
        }

    except Exception as e:
        logger45.error(f"Неожиданная ошибка при запросе к {url}: {e}")
        return {
            "url": url,
            "status": None,
            "content": None,
            "success": False,
            "error": {type(e).__name__}
        }


async def fetch_multiple_websites():
    websites = [
        "https://yandex.com",
        "https://invalid.url",
        "https://miet.ru"
    ]

    logger45.info("Начало запросов")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in websites]
        results = await asyncio.gather(*tasks)

        successful = 0
        failed = 0
        for result in results:
            if result["success"]:
                successful += 1
                print(f"{result['url']}: Статус {result['status']}")
            else:
                failed += 1
                print(f"{result['url']}: Ошибка - {result['error']}")

        print(f"Успешно - {successful}, Неудачно - {failed}")
        return results

async def main():
    print("ЗАДАНИЕ 1\n")
    file_content = await read_file_async('test7.txt')
    print(file_content)

    print("ЗАДАНИЕ 2\n")
    test_data = []
    for i in range(10):
        random_number = random.randint(1, 100)
        test_data.append(random_number)
    logger_main.info(f"Исходные данные: {test_data}")

    try:
        processing_result = await process_data_async(test_data)
        print("Результат обработки:")
        for key, value in processing_result.items():
            print(f"  {key}: {value}")
    except ValueError:
        logger_main.error("Пустые данные")

    print("ЗАДАНИЕ 3\n")
    await multiple_greetings()

    print("ЗАДАНИЯ 4 и 5\n")
    await fetch_multiple_websites()

if __name__ == "__main__":
    asyncio.run(main())