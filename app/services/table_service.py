import logging
from playwright.async_api import Page
from app.config import settings

logger = logging.getLogger("donor_bot")


async def count_rows(page: Page) -> int:
    await page.wait_for_selector(
        settings.TABLE_WRAP_SELECTOR,
        state="visible",
        timeout=settings.TABLE_WAIT_TIMEOUT_MS,
    )
    return await page.locator(settings.ROWS_SELECTOR).count()


async def list_rows(page: Page) -> list[dict]:
    rows = page.locator(settings.ROWS_SELECTOR)
    n = await rows.count()
    result: list[dict] = []
    for i in range(n):
        row = rows.nth(i)
        date_text = (await row.locator(settings.DATE_SELECTOR).inner_text()).strip()
        btn = row.locator(settings.RESERVATION_SELECTOR)
        state = "reservation" if await btn.count() > 0 else "forbidden"
        result.append({"date": date_text, "state": state})
    return result


async def click_reservation(page: Page, index: int) -> bool:
    row = page.locator(settings.ROWS_SELECTOR).nth(index)
    btn = row.locator(settings.RESERVATION_SELECTOR)
    if await btn.count() == 0:
        logger.error("click_reservation: no reservation button in row %d", index)
        return False
    await btn.first.click()
    logger.info("click_reservation: clicked in row %d", index)
    return True