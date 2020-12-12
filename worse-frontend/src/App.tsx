import "./App.less";
import React from "react";
import { Router, Switch, Route } from "react-router-dom";
import history from "./history";
import WorstLayout from "./components/worst-layout";
import OfferTable from "./components/offers/offer-table/offer-table";
import OfferInfo from "./components/offers/offer-info/offer-info";
import TransactionTable from "./components/transactions/transaction-table/transaction-table";
import TransactionInfo from "./components/transactions/transaction-info/transaction-info";
import WelcomePage from "./components/welcome/welcome";

function App() {
  return (
    <Router history={history}>
      <Switch>
        <Route exact path="/">
          <WorstLayout>
            <WelcomePage />
          </WorstLayout>
        </Route>
        <Route exact path="/offers">
          <WorstLayout>
            <OfferTable />
          </WorstLayout>
        </Route>
        <Route exact path="/offers/:id">
          <WorstLayout>
            <OfferInfo />
          </WorstLayout>
        </Route>
        <Route exact path="/transactions">
          <WorstLayout>
            <TransactionTable />
          </WorstLayout>
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
