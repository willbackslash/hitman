import React from 'react';
import { Navbar, NavDropdown, Nav } from 'react-bootstrap';
import PropTypes from 'prop-types';

const Navigation = ({ profile, canViewHitmen }) => (
  <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
    <Navbar.Brand href="#">Hitman</Navbar.Brand>
    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
    <Navbar.Collapse id="responsive-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link href="/hits" active>Hits</Nav.Link>
        {canViewHitmen && <Nav.Link href="/hitmen">Hitmen</Nav.Link> }
      </Nav>
      <Nav>
        <NavDropdown title={profile && profile.email} id="collasible-nav-dropdown">
          <NavDropdown.Item href="/logout">Sign out</NavDropdown.Item>
        </NavDropdown>
      </Nav>
    </Navbar.Collapse>
  </Navbar>
);

Navigation.propTypes = {
  profile: PropTypes.shape({
    email: PropTypes.string,
  }).isRequired,
  canViewHitmen: PropTypes.bool.isRequired,
};

export default Navigation;
