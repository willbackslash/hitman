/* eslint-disable react/jsx-props-no-spreading */
import React, {
  useEffect,
  useState,
} from 'react';

import useAxios from 'axios-hooks';
import PropTypes from 'prop-types';
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
  withRouter,
} from 'react-router-dom';

import Navigation from './components/Navigation';
import useIsAuthenticaded from './hooks/useIsAuthenticated';
import Hitman from './pages/Hitman';
import Hitmen from './pages/Hitmen';
import Hits from './pages/Hits';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Signup from './pages/Signup';
import { hasHitmenPermissions } from './utils';

const PrivateRoute = ({ component: Component, profile, ...props }) => {
  const isAutenticated = useIsAuthenticaded();
  return (
    <Route
      {...props}
      // eslint-disable-next-line no-shadow
      render={(props) => (isAutenticated ? (<Component profile={profile} {...props} />) : (<Redirect to="/" />))}
    />
  );
};

PrivateRoute.propTypes = {
  profile: PropTypes.shape({
    email: PropTypes.string,
  }).isRequired,
  component: PropTypes.element.isRequired,
};

const MainRouter = () => {
  const isAutenticated = useIsAuthenticaded();

  // TODO : handle API errors redirecting to 500 page
  // eslint-disable-next-line no-unused-vars
  const [{ data: userProfile, error }, callProfileService] = useAxios(
    { url: '/users/profile', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } },
    { manual: true },
  );

  const [profile, setProfile] = useState(null);
  const [canViewHitmen, setCanViewHitmen] = useState(null);

  useEffect(
    () => {
      if (isAutenticated) {
        callProfileService();
      }
    }, [isAutenticated, callProfileService],
  );

  useEffect(
    () => {
      if (userProfile) {
        setProfile(userProfile);
      }
    }, [userProfile],
  );

  useEffect(
    () => {
      if (userProfile) {
        setProfile(userProfile);
        setCanViewHitmen(hasHitmenPermissions(userProfile));
      }
    }, [userProfile],
  );

  return (
    <Router>
      {isAutenticated && <Navigation profile={profile} canViewHitmen={canViewHitmen} />}
      <Switch>
        <Route path="/" component={withRouter(Login)} exact />
        <Route path="/register" component={withRouter(Signup)} exact />
        <PrivateRoute path="/hits" component={withRouter(Hits)} profile={profile} exact />
        <PrivateRoute path="/hitmen" component={withRouter(Hitmen)} profile={profile} exact />
        <PrivateRoute path="/hitmen/:hitmanId" component={withRouter(Hitman)} profile={profile} exact />
        <PrivateRoute path="/logout" component={withRouter(Logout)} exact />
        <Route>
          <h2>404: Target not found</h2>
        </Route>
      </Switch>
    </Router>
  );
};
export default MainRouter;
