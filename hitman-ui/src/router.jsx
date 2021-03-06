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
} from 'react-router-dom';

import Navigation from './components/Navigation';
import useIsAuthenticaded from './hooks/useIsAuthenticated';
import CreateHit from './pages/CreateHit';
import Hitman from './pages/Hitman';
import Hitmen from './pages/Hitmen';
import Hits from './pages/Hits';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Page404 from './pages/Page404';
import Signup from './pages/Signup';
import {
  hasHitmenPermissions,
  isBoss,
  isManager,
} from './utils';

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
        setCanViewHitmen(hasHitmenPermissions(userProfile));
      }
    }, [userProfile],
  );

  return (
    <Router>
      {isAutenticated && <Navigation profile={profile} canViewHitmen={canViewHitmen} />}
      <Switch>
        <Route path="/" component={Login} exact />
        <Route path="/register" component={Signup} exact />
        <PrivateRoute path="/hits" component={Hits} profile={profile} exact />
        {profile && (isBoss(profile) || isManager(profile)) && (
        <>
          <PrivateRoute path="/hits/add" component={CreateHit} profile={profile} exact />
          <PrivateRoute path="/hitmen" component={Hitmen} profile={profile} exact />
          <PrivateRoute path="/hitmen/:hitmanId" component={Hitman} profile={profile} exact />
        </>
        )}
        <PrivateRoute path="/logout" component={Logout} exact />
        <Route component={Page404} />
      </Switch>
    </Router>
  );
};
export default MainRouter;
