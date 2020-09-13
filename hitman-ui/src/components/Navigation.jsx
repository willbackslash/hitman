import React from 'react';
import { Navbar, NavDropdown, Nav } from 'react-bootstrap';
import PropTypes from 'prop-types';

const Navigation = ({ onSignOut }) => (
  <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
    <Navbar.Brand href="#">Hitman</Navbar.Brand>
    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
    <Navbar.Collapse id="responsive-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link href="/hits" active>Hits</Nav.Link>
        <Nav.Link href="/hitmen">Hitmen</Nav.Link>
      </Nav>
      <Nav>
        <NavDropdown title="myhitmail@email.com" id="collasible-nav-dropdown">
          <NavDropdown.Item href="#" onClick={onSignOut}>Sign out</NavDropdown.Item>
        </NavDropdown>
      </Nav>
    </Navbar.Collapse>
  </Navbar>
);

Navigation.propTypes = {
  onSignOut: PropTypes.func.isRequired,
};

export default Navigation;
