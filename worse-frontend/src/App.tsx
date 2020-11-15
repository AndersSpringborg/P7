import React from "react";
import { Router, Switch, Route } from "react-router-dom";
import history from "./history";
import "./App.css";
import WorstLayout from "./components/worst-layout";
import OfferTable from "./components/offers/offer-table/offer-table";
import WineInfo from "./components/offers/offer-info/offer-info";
import TransactionTable from "./components/transactions/transaction-table/transaction-table";

function App() {
  return (
    <Router history={history}>
      <Switch>
        <Route exact path="/">
          <WorstLayout>
            <OfferTable />
          </WorstLayout>
        </Route>
        <Route exact path="/wineOffer/:id">
          <WorstLayout>
            <WineInfo />
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
