/**
    Stream Marker API
    Copyright (C) 2022 Marc Steele
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';

const Menu = (): React.ReactElement => {
    return (
        <Navbar>
            <Container>
                <Navbar.Brand>Shoutcast Metadata Converter</Navbar.Brand>
                <Navbar.Toggle aria-controls='main-nav' />
                <Navbar.Collapse id="main-nav">
                    <Nav>
                        <Nav.Link href="#">Step 1</Nav.Link>
                        <Nav.Link href="#">Step 2</Nav.Link>
                        <Nav.Link href="#">Step 3</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}

export default Menu;