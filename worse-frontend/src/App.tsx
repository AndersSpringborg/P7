import React from "react";
import { Router, Switch, Route } from "react-router-dom";
import history from "./history";
import "./App.css";
import WineOfferList from "./components/wine-offer-list";

function App() {
  return (
    <Router history={history}>
      <Switch>
        <Route exact path="/">
          <WineOfferList />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
