/// <reference types="cypress"></reference>;

describe("Traversing the WORST UI", () => {
  beforeEach(() => {
    cy.visit("http://localhost:3000/");
  });

  it("Enter Offers", () => {
    cy.contains("Wine Offer Recommendations");
  });

  it("Enter Transactions", () => {
    cy.contains("Transactions").click();
    cy.contains("Previous Transactions");

    cy.get("th").eq(0).should("contain", "Vendor Id");
    cy.get("th").eq(1).should("contain", "Description");
    cy.get("th").eq(2).should("contain", "LWIN");
    cy.get("th").eq(3).should("contain", "Price");
    cy.get("th").eq(0).get("span").eq(9).click();
  });

  it("Search Transactions", () => {
    cy.contains("Transactions").click();
    cy.get("th")
      .eq(0)
      .get("span")
      .eq(9)
      .click()
      .get("input")
      .type("Bourgogne")
      .get("button")
      .eq(3)
      .click()
      .get("p")
      .contains("No Data")
      .should("be.visible");
  });

  it("Reset Search Transactions", () => {
    cy.contains("Transactions").click();
    cy.get("th")
      .eq(0)
      .get("span")
      .eq(9)
      .click()
      .get("input")
      .type("Bourgogne")
      .get("button")
      .eq(3)
      .click();

    cy.get("th")
      .eq(0)
      .get("span")
      .eq(9)
      .click()
      .get("input")
      .get("button")
      .eq(2)
      .click();
  });
});
