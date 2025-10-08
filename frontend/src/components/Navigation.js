import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';

const Nav = styled.nav`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const NavList = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  gap: 2rem;
`;

const NavItem = styled.li`
  margin: 0;
`;

const NavLink = styled(Link)`
  text-decoration: none;
  color: ${props => props.active ? '#667eea' : '#2c3e50'};
  font-weight: ${props => props.active ? '600' : '500'};
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: ${props => props.active ? 'rgba(102, 126, 234, 0.1)' : 'transparent'};
  
  &:hover {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
  }
`;

const Navigation = () => {
  const location = useLocation();

  return (
    <Nav>
      <NavList>
        <NavItem>
          <NavLink 
            to="/" 
            active={location.pathname === '/' ? 1 : 0}
          >
            Dashboard
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink 
            to="/predict" 
            active={location.pathname === '/predict' ? 1 : 0}
          >
            Risk Assessment
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink 
            to="/results" 
            active={location.pathname === '/results' ? 1 : 0}
          >
            Results
          </NavLink>
        </NavItem>
      </NavList>
    </Nav>
  );
};

export default Navigation;
