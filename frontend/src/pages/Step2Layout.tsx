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
import { Container, Spinner } from 'react-bootstrap';


interface Props {
    showSpinner: boolean;
}

const Step2Layout = ({ children, showSpinner }: React.PropsWithChildren<Props>): React.ReactElement => {
    return (
        <Container>
            <h1>Step 2</h1>
            <p>In this step we perform the actual capture from the network.</p>
            {showSpinner && (
                <Spinner animation="border" variant="primary" />
            )}
            {children}
        </Container>
    )
}

export default Step2Layout;