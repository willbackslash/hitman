import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom';
import Login from './pages/Login';
import Hits from './pages/Hits';

const PublicRoutes = () => (
  <Switch>
    <Route path="/" exact>
      <Login />
    </Route>
  </Switch>
);

const PrivateRoutes = () => (
  <Switch>
    <Route path="/hits" exact>
      <Hits />
    </Route>
  </Switch>
);

const MainRouter = () => (
  <Router>
    <PrivateRoutes />
    <PublicRoutes />
  </Router>
);

export default MainRouter;
