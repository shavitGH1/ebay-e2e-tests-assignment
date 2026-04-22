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
            await self.page.pause()
            with allure.step(f"Filtering price between 1 and {max_price}"):
                if await self.page.is_visible(self.price_input_min):
                    await self.utils.fill_element(self.price_input_min, "1")
                    await self.utils.fill_element(self.price_input_max, str(max_price))
                    if await self.page.is_enabled(self.price_submit_button):
                        await self.page.click(self.price_submit_button)
                        await self.page.wait_for_load_state("networkidle")

            item_urls: List[str] = []
            while len(item_urls) < limit:
                await self.wait_for_selector(self.item_container)
                items = await self.page.query_selector_all(self.item_container)
                for item in items:
                    price_text = ""
                    url = ""

                    # Try new s-card layout first
                    price_el = await item.query_selector(".s-card__price")
                    url_el = await item.query_selector(".su-card-container__header > a.s-card__link")

                    if price_el and url_el:
                        price_text = await price_el.inner_text()
                        url = await url_el.get_attribute('href')
                    else:
                        # Fallback to old s-item layout
                        price_el = await item.query_selector(".s-item__price")
                        url_el = await item.query_selector(".s-item__info > a.s-item__link")
                        if price_el and url_el:
                            price_text = await price_el.inner_text()
                            url = await url_el.get_attribute('href')

                    if not price_text or not url:
                        continue

                    try:
                        # Use regex to find the first number (int or float) in the string
                        price_match = re.search(r'[\d,.]+', price_text)
                        if not price_match:
                            continue
                        
                        price = float(price_match.group(0).replace(',', ''))

                        if 1 <= price <= max_price:
                            if url and url not in item_urls:
                                item_urls.append(url)
                                if len(item_urls) >= limit:
                                    break
                    except (ValueError, TypeError):
                        continue
                
                if len(item_urls) < limit and await self.page.is_visible(self.next_page_button):
                    await self.utils.click_element(self.next_page_button)
                else:
                    break
            
            allure.attach(str(item_urls), name="Collected URLs", attachment_type=allure.attachment_type.TEXT)
            return item_urls[:limit]
