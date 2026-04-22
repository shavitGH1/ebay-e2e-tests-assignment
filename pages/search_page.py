import allure
from typing import List
from playwright.async_api import Page
from pages.base_page import BasePage


class SearchPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_input: str = "#gh-ac"
        self.search_button: str = "#gh-search-btn"
        self.item_container: str = "//div[@id='srp-river-results']//li[contains(@class, 's-item')]"
        self.price_input_min: str = "input[aria-label='Minimum Value in $']"
        self.price_input_max: str = "input[aria-label='Maximum Value in $']"
        self.price_submit_button: str = "button[aria-label='Submit price range']"
        self.next_page_button: str = "a[aria-label='Go to next search page']"

    async def search_items_by_name_under_price(self, query: str, max_price: float, limit: int) -> List[str]:
        with allure.step(f"Searching for '{query}' with max price ${max_price}"):
            await self.utils.fill_element(self.search_input, query)
            await self.utils.click_element(self.search_button)

            if await self.page.is_visible(self.price_input_max):
                await self.utils.fill_element(self.price_input_max, str(max_price))
                await self.utils.click_element(self.price_submit_button)

            item_urls: List[str] = []
            while len(item_urls) < limit:
                await self.wait_for_selector(self.item_container)
                items = await self.page.query_selector_all(self.item_container)
                for item in items:
                    price_text_element = await item.query_selector(".s-item__price")
                    if price_text_element:
                        price_text = await price_text_element.inner_text()
                        try:
                            price = float(price_text.replace('$', '').split(' to ')[0])
                            if price <= max_price:
                                url_element = await item.query_selector(".s-item__link")
                                if url_element:
                                    url = await url_element.get_attribute('href')
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
