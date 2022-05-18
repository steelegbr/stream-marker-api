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

import React, { useCallback, useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import validator from 'validator';

interface UrlEntryStatus {
    valid: boolean;
    url: string;
}

const UrlEntryForm = (): React.ReactElement => {
    const [formStatus, setFormStatus] = useState<UrlEntryStatus>({
        valid: false,
        url: ''
    });

    const updateUrl = useCallback(
        (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
            const url = event.target.value;
            setFormStatus({
                valid: validator.isURL(url),
                url: url
            });
        },
        [setFormStatus]
    )
    return (
        <Form>
            <Form.Group className="mb-3" controlId="url">
                <Form.Label>Stream URL</Form.Label>
                <Form.Control type="url" placeholder="Enter Stream URL" value={formStatus.url} onChange={updateUrl} />
            </Form.Group>
            <Button variant="primary" type="submit" disabled={!formStatus.valid}>
                Capture
            </Button>
        </Form>
    )
}

export default UrlEntryForm;