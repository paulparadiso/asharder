import React, { useContext } from 'react';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Slider from '@mui/material/Slider';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider';
import Keyboard from 'react-simple-keyboard';
import RecordingControls from './RecordingControls';
import ProjectControls from './ProjectControls';
import AudioControls from './AudioControls';
import FileDisplay from './FileDisplay';

const defaultTheme = createTheme({
    palette: {
        mode: 'dark'
    }
});

const Main = props => {

    const [state, dispatch] = useContext(AudioParameterContext);

    return (
        <ThemeProvider theme={defaultTheme}>
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    height: '100vh',
                    width: '100vw',
                    overflow: 'auto',
                }}
            >
                <CssBaseline />
                <Container maxWidth="lg" sx={{ mt: 4, mb: 4, margin: 0 }}>
                    <Grid container>
                        <Grid item lg={6} sx={{ mt: 10 }}>
                            <RecordingControls />
                        </Grid>
                        <Grid item lg={6} sx={{ mt: 4 }}>
                            <ProjectControls />
                            <FileDisplay />

                        </Grid>
                    </Grid>
                    <Grid container>
                        <AudioControls />
                    </Grid>
                </Container >
            </Box>
        </ThemeProvider>
    );

}

export default Main;