import allure
import re
import random
from typing import List
from playwright.async_api import Page
from pages.base_page import BasePage
from utils.wait_utils import random_async_wait, human_like_click

class SearchPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_input: str = "#gh-ac"
        self.search_button: str = "#gh-search-btn"
        self.item_container: str = "//ul[contains(@class, 'srp-results')]/li[@data-listingid]"
        self.price_input_min: str = "input[aria-label*='Minimum Value']"
        self.price_input_max: str = "input[aria-label*='Maximum Value']"
        self.price_submit_button: str = "button[aria-label='Submit price range']"
        self.next_page_button: str = "a[aria-label='Go to next search page']"

    async def search_items_by_name_under_price(self, query: str, max_price: float, limit: int) -> List[str]:
        with allure.step(f"Searching for '{query}' with max price ${max_price}"):
            await self.page.type(self.search_input, query, delay=random.randint(50, 150))
            await random_async_wait()
            await human_like_click(self.page, self.search_button)
            await random_async_wait()

            with allure.step(f"Filtering price between 1 and {max_price}"):
                if await self.page.is_visible(self.price_input_min):
                    await self.page.type(self.price_input_min, "1", delay=random.randint(50, 150))
                    await random_async_wait()
                    await self.page.type(self.price_input_max, str(max_price), delay=random.randint(50, 150))
                    await random_async_wait()
                    if await self.page.is_enabled(self.price_submit_button):
                        await human_like_click(self.page, self.price_submit_button)
                        await self.page.wait_for_load_state("networkidle")

            item_urls: List[str] = []
            while len(item_urls) < limit:
                await self.wait_for_selector(self.item_container)
                items = await self.page.query_selector_all(self.item_container)
                for item in items:
                    price_text_element = await item.query_selector(".s-card__price, .s-item__price")

                    if price_text_element:
                        price_text = await price_text_element.inner_text()
                        price_match = re.search(r'[\d,]+\.\d{2}', price_text.replace(',', ''))
                        if not price_match:
                            continue

                        price = float(price_match.group(0))

                        if 1 <= price <= max_price:
                            url_element = await item.query_selector("a.s-card__link, a.s-item__link")

                            if url_element:
                                url = await url_element.get_attribute('href')
                                if url and url not in item_urls:
                                    item_urls.append(url)
                                    if len(item_urls) >= limit:
                                        break

                if len(item_urls) < limit and await self.page.is_visible(self.next_page_button):
                    await human_like_click(self.page, self.next_page_button)
                    await random_async_wait()
                else:
                    break

            allure.attach(str(item_urls), name="Collected URLs", attachment_type=allure.attachment_type.TEXT)
            return item_urls[:limit]
