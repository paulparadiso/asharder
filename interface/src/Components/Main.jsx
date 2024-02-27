import React, { useContext } from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import Grid from '@mui/material/Grid';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider';
import Keyboard from 'react-simple-keyboard';
import RecordingControls from './RecordingControls';
import ProjectControls from './ProjectControls';
import AudioControls from './AudioControls';
import FileDisplay from './FileDisplay';

const Main = props => {

    const [state, dispatch] = useContext(AudioParameterContext);

    return (
        <Grid container>
            <Grid item lg={6}>
                <RecordingControls />
            </Grid>
            <Grid item lg={6}>
                <ProjectControls />
                <FileDisplay />
                <AudioControls />
            </Grid>
        </Grid>
    );

}

export default Main;