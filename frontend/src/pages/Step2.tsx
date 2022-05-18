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

import { AxiosResponse } from 'axios';
import React, { useCallback, useState } from 'react';
import { Alert, Container } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { streamAudio } from '../api/CaptureAPI';
import { Capture } from '../model/Capture';
import Step2Layout from './Step2Layout';

type ProcessStatus = 'Capturing' | 'Stopping' | 'Error' | 'AxiosError';

const KEY_BITRATE = 'icy-br';
const KEY_META_INTERVAL = 'icy-metaint';

const Step2 = (): React.ReactElement => {
    const { id } = useParams();
    const fromLocalStorage = localStorage.getItem(id || '') || '{}';
    const [capture, setCapture] = useState<Capture>(JSON.parse(fromLocalStorage));
    const [status, setStatus] = useState<ProcessStatus>('Capturing');

    const captureCallback = useCallback(
        (progressEvent: any) => {
            console.log(progressEvent);
        },
        []
    )

    // Error handling

    if (!capture.url) {
        return (
            <Container>
                <h1>Step 2</h1>
                <Alert key='danger' variant='danger'>Failed to loacate the specified capture. Please try again from step 1.</Alert>
            </Container>
        )
    }

    if (status == 'Error') {
        return (
            <Step2Layout showSpinner={false}>
                <Alert key='danger' variant='danger'>Something went wrong. Please try again.</Alert>
            </Step2Layout>
        )
    }

    if (status == 'AxiosError') {
        return (
            <Step2Layout showSpinner={false}>
                <Alert key='danger' variant='danger'>Failed to obtain audio from the URL given. Please check the URL is valid and the same security level (HTTP or HTTPS) as this website.</Alert>
            </Step2Layout>
        )
    }

    // Perform the capture

    if (status == 'Capturing') {
        streamAudio(capture, captureCallback).then(
            (response: AxiosResponse) => {

                // Happy response from the server?

                if (response.status === 200 && KEY_BITRATE in response.headers && KEY_META_INTERVAL in response.headers) {
                    console.log(response.headers);
                } else {
                    setStatus('Error');
                }

            },
            (error) => {
                console.log(`Capture error: ${error}`);
                console.log(error);
                setStatus('AxiosError');
            }
        );
        return (
            <Step2Layout showSpinner={true}>Capturing audio...</Step2Layout>
        )
    }

    return (
        <Step2Layout showSpinner={false}>...</Step2Layout>
    )
}

export default Step2;