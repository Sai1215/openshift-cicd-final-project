Feature: Product catalogue administration
  As an administrator
  I want to manage products
  So that the catalogue remains accurate

  Background:
    Given the product catalogue contains
      | name         | description         | price | category | available |
      | Red Apple    | Fresh red apple     | 1.50  | Fruit    | true      |
      | Orange Juice | Fresh orange juice  | 3.00  | Drinks   | false     |
      | Green Tea    | Organic green tea   | 2.50  | Drinks   | true      |

  Scenario: Read a product
    When I visit the "Home Page"
    And I open the product "Red Apple"
    Then I should see the product details for "Red Apple"

  Scenario: Update a product
    When I update the product "Red Apple" to "Updated Red Apple"
    Then I should see the product details for "Updated Red Apple"

  Scenario: Delete a product
    When I delete the product "Red Apple"
    Then the product "Red Apple" should not be listed

  Scenario: List all products
    When I visit the "Home Page"
    Then I should see all three products

  Scenario: Search products by name
    When I visit the "Home Page"
    And I search for product "Red"
    Then I should see product "Red Apple" in the results
    And I should not see product "Orange Juice" in the results

  Scenario: Search products by category
    When I visit the "Home Page"
    And I filter products by category "Drinks"
    Then I should see product "Orange Juice" in the results
    And I should see product "Green Tea" in the results

  Scenario: Search products by availability
    When I visit the "Home Page"
    And I filter products by availability "true"
    Then I should see product "Red Apple" in the results
    And I should see product "Green Tea" in the results
    And I should not see product "Orange Juice" in the results
