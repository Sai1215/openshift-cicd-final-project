from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


@when('I visit the "{page}"')
def visit_page(context, page):
    pages = {"Home Page": "/"}
    if page not in pages:
        raise AssertionError(f"Unknown page: {page}")
    context.driver.get(context.base_url + pages[page])


@when('I open the product "{name}"')
def open_product(context, name):
    context.driver.find_element(By.LINK_TEXT, name).click()


@then('I should see the product details for "{name}"')
def see_product_details(context, name):
    heading = context.driver.find_element(By.ID, "product-name")
    assert heading.text == name


@when('I update the product "{old_name}" to "{new_name}"')
def update_product(context, old_name, new_name):
    context.driver.get(context.base_url + "/")
    context.driver.find_element(By.LINK_TEXT, old_name).click()
    field = context.driver.find_element(By.NAME, "name")
    field.clear()
    field.send_keys(new_name)
    context.driver.find_element(By.ID, "save-update").click()


@when('I delete the product "{name}"')
def delete_product(context, name):
    context.driver.get(context.base_url + "/")
    product = context.driver.find_element(
        By.CSS_SELECTOR,
        f'[data-product-name="{name}"]',
    )
    product.find_element(By.CSS_SELECTOR, "button").click()


@then('the product "{name}" should not be listed')
def product_not_listed(context, name):
    assert name not in context.driver.page_source


@then("I should see all three products")
def see_all_products(context):
    for name in ("Red Apple", "Orange Juice", "Green Tea"):
        assert name in context.driver.page_source


@when('I search for product "{name}"')
def search_by_name(context, name):
    field = context.driver.find_element(By.NAME, "q")
    field.clear()
    field.send_keys(name)
    context.driver.find_element(By.CSS_SELECTOR, "#search-form button").click()


@when('I filter products by category "{category}"')
def filter_by_category(context, category):
    Select(context.driver.find_element(By.NAME, "category")).select_by_visible_text(category)
    context.driver.find_element(By.CSS_SELECTOR, "#search-form button").click()


@when('I filter products by availability "{availability}"')
def filter_by_availability(context, availability):
    Select(context.driver.find_element(By.NAME, "availability")).select_by_value(availability)
    context.driver.find_element(By.CSS_SELECTOR, "#search-form button").click()


@then('I should see product "{name}" in the results')
def product_in_results(context, name):
    context.driver.find_element(
        By.CSS_SELECTOR,
        f'[data-product-name="{name}"]',
    )


@then('I should not see product "{name}" in the results')
def product_not_in_results(context, name):
    assert f'data-product-name="{name}"' not in context.driver.page_source


@when('I click the "{button}" button')
def click_button(context, button):
    context.driver.find_element(
        By.XPATH,
        f'//button[normalize-space()="{button}"]',
    ).click()


@then('I should see the message "{message}"')
def see_message(context, message):
    assert message in context.driver.page_source
