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
import { Container } from 'react-bootstrap';
import { Route, Routes } from 'react-router-dom';
import Paths from '../components/Paths';
import UrlEntryForm from '../components/UrlEntryForm';

const Step1 = (): React.ReactElement => {
    return (
        <Container>
            <h1>Step 1</h1>
            <p>In this step you supply a stream URL and we capture it to your hard disk.</p>
            <Routes>
                <Route
                    element={(
                        <UrlEntryForm />
                    )}
                    path={Paths.step1.basePath}
                />
            </Routes>
            
        </Container>
    )
}

export default Step1;