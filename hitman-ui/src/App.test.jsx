/* eslint-disable no-undef */
import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('it renders login page', () => {
  const { getByText } = render(<App />);
  const linkElement = getByText('Welcome to Hitman');
  expect(linkElement).toBeInTheDocument();
});
