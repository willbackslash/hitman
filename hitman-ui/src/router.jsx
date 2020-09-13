import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route, useHistory, withRouter,
} from 'react-router-dom';
import Navigation from './components/Navigation';
import Login from './pages/Login';
import Hits from './pages/Hits';
import useIsAuthenticaded from './hooks/useIsAuthenticated';

const PrivateRoutes = () => {
  const isAutenticated = useIsAuthenticaded();
  const history = useHistory();
  const onSignOut = () => {
    sessionStorage.removeItem('SESSION_AUTH');
    history.push('/');
    window.location.reload();
  };

  return (
    isAutenticated
      ? (
        <>
          <Navigation onSignOut={onSignOut} />
          <Switch>
            <Route path="/hits" component={withRouter(Hits)} exact />
            <Route path="/hitmen" component={withRouter(Hits)} exact />
          </Switch>
        </>
      ) : null
  );
};

const PublicRoutes = () => (
  <Switch>
    <Route path="/" component={withRouter(Login)} exact />
  </Switch>
);

const MainRouter = () => (
  <Router>
    <PrivateRoutes />
    <PublicRoutes />
  </Router>
);
export default MainRouter;
