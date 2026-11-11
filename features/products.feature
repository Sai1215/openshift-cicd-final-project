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
    When I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    And I copy the product ID for "Red Apple"
    And I paste the copied ID into the "Product ID" field
    And I press the "Retrieve" button
    Then I should see "Red Apple" in the search results
    And I should see "Fresh red apple" in the search results
    And I should see "1.50" in the search results
    And I should see "Fruit" in the search results
    And I should see "Available" in the search results

  Scenario: Update a product
    When I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    And I copy the product ID for "Red Apple"
    And I paste the copied ID into the "Product ID" field
    And I enter "Updated Red Apple" into the "Name" field
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I enter "Updated Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should see "Updated Red Apple" in the search results
    When I press the "Clear" button
    And I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should not see "Red Apple" in the search results

  Scenario: Delete a product
    When I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    And I copy the product ID for "Red Apple"
    And I paste the copied ID into the "Product ID" field
    And I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should not see "Red Apple" in the search results

  Scenario: List all products
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Red Apple" in the search results
    And I should see "Orange Juice" in the search results

  Scenario: Search products by category
    When I press the "Clear" button
    And I select "Drinks" from the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Orange Juice" in the search results
    And I should see "Green Tea" in the search results
    And I should not see "Red Apple" in the search results

  Scenario: Search products by availability
    When I press the "Clear" button
    And I select "Available" from the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Red Apple" in the search results
    And I should see "Green Tea" in the search results
    And I should not see "Orange Juice" in the search results

  Scenario: Search products by name
    When I press the "Clear" button
    And I enter "Red Apple" into the "Search Name" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Red Apple" in the search results
    And I should not see "Orange Juice" in the search results
