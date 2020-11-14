import React from "react";
import { Router, Switch, Route } from "react-router-dom";
import history from "./history";
import "./App.css";
import WineOfferList from "./components/wine-offer-list";
import OfferTable from "./components/offer-table/offer-table";
import WineInfo from "./components/offer-info/offer-info";

function App() {
  return (
    <Router history={history}>
      <Switch>
        <Route exact path="/">
          <WineOfferList>
            <OfferTable />
          </WineOfferList>
        </Route>
        <Route exact path="/wineOffer/:id">
          <WineOfferList>
            <WineInfo></WineInfo>
          </WineOfferList>
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
