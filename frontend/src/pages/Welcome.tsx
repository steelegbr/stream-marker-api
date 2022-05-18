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

import React, { useCallback } from 'react';
import { Button, Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import Paths from '../components/Paths';

const Welcome = (): React.ReactElement => {
    const navigate = useNavigate();

    const startProcess = useCallback(
        () => {
            navigate(Paths.step1.base);
        },
        [navigate]
    );

    return (
        <Container>
            <h1>Welcome</h1>
            <p>This tool captures Shoutcast streams with metadata and converts them to wave files with markers. This allows you to tune marker delays for things like ad break triggers.</p>
            <p>We strongly recommend starting with the first step:</p>
            <Button variant="primary" onClick={startProcess}>Begin step 1</Button>
        </Container>
    )
}

export default Welcome;