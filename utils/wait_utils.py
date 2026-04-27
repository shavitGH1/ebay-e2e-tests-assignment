import asyncio
import random
from playwright.async_api import Page

async def random_async_wait(min_ms: int = 1000, max_ms: int = 2500):
    """Waits for a random amount of time between min_ms and max_ms."""
    sleep_time_s = random.randint(min_ms, max_ms) / 1000.0
    await asyncio.sleep(sleep_time_s)

async def human_like_click(page: Page, selector: str):
    """Performs a more human-like click on an element, scrolling if necessary."""
    element = page.locator(selector)
    
    await element.scroll_into_view_if_needed()
    
    box = await element.bounding_box()
    
    if not box:
        await element.click()
        return

    target_x = box['x'] + (box['width'] * random.uniform(0.2, 0.8))
    target_y = box['y'] + (box['height'] * random.uniform(0.2, 0.8))

    await page.mouse.move(target_x, target_y, steps=random.randint(50, 80))
    await asyncio.sleep(random.uniform(0.2, 0.5))
    await page.mouse.click(target_x, target_y, delay=random.randint(100, 200))
