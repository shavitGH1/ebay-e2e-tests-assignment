import allure
import re
from typing import List
from playwright.async_api import Page
from pages.base_page import BasePage


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
            await self.utils.fill_element(self.search_input, query)
            await self.utils.click_element(self.search_button)

            with allure.step(f"Filtering price between 1 and {max_price}"):
                if await self.page.locator(self.price_input_min).is_visible():
                    await self.utils.fill_element(self.price_input_min, "1")
                    await self.utils.fill_element(self.price_input_max, str(max_price))
                    if await self.page.locator(self.price_submit_button).is_enabled():
                        await self.utils.click_element(self.price_submit_button)

            item_urls: List[str] = []
            while len(item_urls) < limit:
                await self.page.locator(self.item_container).first.wait_for()
                items = await self.page.locator(self.item_container).all()
                for item in items:
                    price_text_element = item.locator(".s-card__price, .s-item__price")

                    if await price_text_element.count() > 0:
                        price_text = await price_text_element.first.inner_text()
                        price_match = re.search(r'[\d,]+\.\d{2}', price_text.replace(',', ''))
                        if not price_match:
                            continue

                        price = float(price_match.group(0))

                        if 1 <= price <= max_price:
                            url_element = item.locator("a.s-card__link, a.s-item__link")

                            if await url_element.count() > 0:
                                url = await url_element.first.get_attribute('href')
                                if url and url not in item_urls:
                                    item_urls.append(url)
                                    if len(item_urls) >= limit:
                                        break

                if len(item_urls) < limit and await self.page.locator(self.next_page_button).is_visible():
                    await self.utils.click_element(self.next_page_button)
                else:
                    break

            allure.attach(str(item_urls), name="Collected URLs", attachment_type=allure.attachment_type.TEXT)
            return item_urls[:limit]
