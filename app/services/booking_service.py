import logging
import time
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from app.config import settings
from app.services.table_service import count_rows, list_rows, click_reservation
from app.services.time_service import now_msk, deadline_after, jitter_sleep

logger = logging.getLogger("donor_bot")


async def booking_loop(page: Page) -> bool:
    """Снимок → цикл рефреша до target → клик. Возвращает True если кликнули."""
    initial_count = await count_rows(page)
    target = initial_count + 1
    logger.info("booking_loop: snapshot count=%d, target=%d", initial_count, target)
    logger.debug("booking_loop: rows=%s", await list_rows(page))
    deadline = deadline_after(settings.TIMEOUT_MIN)
    logger.info("booking_loop: deadline=%s", deadline.strftime("%H:%M:%S"))
    i = 0
    n = initial_count
    while now_msk() < deadline:
        i += 1
        t = time.perf_counter()
        try:
            await page.reload(wait_until="commit")
            n = await count_rows(page)
        except PlaywrightTimeoutError as e:
            logger.warning("booking_loop: reload #%d timeout: %s (took=%.2fs)", i, e, time.perf_counter() - t)
            jitter_sleep()
            continue
        took = time.perf_counter() - t
        logger.debug("booking_loop: reload #%d count=%d (target=%d) took=%.2fs", i, n, target, took)
        logger.debug("booking_loop: rows=%s", await list_rows(page))
        if n == target:
            logger.info("booking_loop: target reached at reload #%d (count=%d)", i, n)
            ok = await click_reservation(page, initial_count)
            logger.info("booking_loop: click result=%s", ok)

            #временное решение для сохранения полного html
            
            html = await page.content()
            with open("account_page.html", "w", encoding="utf-8") as f:
                f.write(html)

            # удаляем
            return ok
        if n > target:
            logger.warning("booking_loop: count=%d > target=%d, clicking last row", n, target)
            ok = await click_reservation(page, n - 1)
            logger.info("booking_loop: click result=%s", ok)
            return ok
        jitter_sleep()

    logger.error("booking_loop: TIMEOUT after %d reloads, last count=%d (target=%d)", i, n, target)
    return False
    
    