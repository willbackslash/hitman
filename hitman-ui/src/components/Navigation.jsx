import React from 'react';

import PropTypes from 'prop-types';
import {
  Nav,
  Navbar,
  NavDropdown,
} from 'react-bootstrap';
import { useLocation } from 'react-router-dom';

const Navigation = ({ profile, canViewHitmen }) => {
  const location = useLocation();
  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
      <Navbar.Brand href="#">Hitman</Navbar.Brand>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/hits" active={location.pathname === '/hits'}>Hits</Nav.Link>
          {canViewHitmen && <Nav.Link href="/hitmen" active={location.pathname === '/hitmen'}>Hitmen</Nav.Link> }
        </Nav>
        <Nav>
          <NavDropdown title={profile && profile.email} id="collasible-nav-dropdown">
            <NavDropdown.Item href="/logout">Sign out</NavDropdown.Item>
          </NavDropdown>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

Navigation.propTypes = {
  profile: PropTypes.shape({
    email: PropTypes.string,
  }).isRequired,
  canViewHitmen: PropTypes.bool.isRequired,
};

export default Navigation;
