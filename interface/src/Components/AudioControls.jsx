import React, { useContext } from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider';

const AudioControls = props => {

    const [state, dispatch] = useContext(AudioParameterContext);

    const sendCommand = command => {
        dispatch({
            type: 'SEND_LOOPER_COMMAND',
            payload: {'command': command}
        })
    }

    const styles = {
        margin: 5,
    };

    return (
        <Grid item lg={12} sx={{ mt: 10 }}>
            <Paper>
                <Button variant="outlined" sx={styles} 
                        onClick={() => sendCommand('randomLoop')}>
                    Shuffle
                </Button>
                <Button variant="outlined" sx={styles}
                        onClick={() => sendCommand('playLoop')}>
                    Play
                </Button>
                <Button variant="outlined" sx={styles}
                        onClick={() => sendCommand('record')}>
                    Record
                </Button>
                <Button variant="outlined" sx={styles} 
                        onClick={() => sendCommand('erase')}>
                    Erase
                </Button>
                <Button variant="outlined" sx={styles}
                        onClick={() => sendCommand('send')}>
                    Send
                </Button>
                <Button variant="outlined" sx={styles}
                        onClick={() => sendCommand('save')}>
                    Save
                </Button>
            </Paper>
        </Grid>
    )

}

export default AudioControls;