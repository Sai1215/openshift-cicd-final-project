from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


@when('I visit the "{page}"')
def visit_page(context, page):
    pages = {"Home Page": "/"}
    if page not in pages:
        raise AssertionError(f"Unknown page: {page}")
    context.driver.get(context.base_url + pages[page])


@when('I enter "{value}" into the "{field}" field')
def enter_field(context, value, field):
    fields = {
        "Search Name": "search_name",
        "Name": "product_name",
        "Product ID": "product_id",
    }
    element = context.driver.find_element(By.ID, fields[field])
    element.clear()
    element.send_keys(value)


@when('I select "{value}" from the "{field}" dropdown')
def select_dropdown(context, value, field):
    fields = {
        "Category": "category",
        "Available": "available",
    }
    element = context.driver.find_element(By.ID, fields[field])
    Select(element).select_by_visible_text(value)


@when('I press the "{button}" button')
def press_button(context, button):
    context.driver.find_element(
        By.XPATH,
        f'//button[normalize-space()="{button}"]',
    ).click()


@when('I copy the product ID for "{name}"')
def copy_product_id(context, name):
    result = context.driver.find_element(
        By.CSS_SELECTOR,
        f'[data-product-name="{name}"] .product-id',
    )
    context.copied_product_id = result.text.strip()


@when('I paste the copied ID into the "{field}" field')
def paste_product_id(context, field):
    if field != "Product ID":
        raise AssertionError(f"Unsupported target field: {field}")
    element = context.driver.find_element(By.ID, "product_id")
    element.clear()
    element.send_keys(context.copied_product_id)


@then('I should see "{text}" in the search results')
def verify_text_present(context, text):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert text in results.text, f"Expected '{text}' in search results: {results.text}"


@then('I should not see "{text}" in the search results')
def verify_text_absent(context, text):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert text not in results.text, f"Did not expect '{text}' in search results: {results.text}"


@then('I should see the message "{message}"')
def see_message(context, message):
    flash_message = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash_message"))
    )
    assert message in flash_message.text


@then('I should see the product details for "{name}"')
def see_product_details(context, name):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert name in results.text
