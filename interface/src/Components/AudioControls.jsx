import React, { useContext, useState } from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider';

const AudioControls = props => {

    const [state, dispatch] = useContext(AudioParameterContext);
    const [recordTime, setRecordTime] = useState('');

    const sendCommand = command => {
        dispatch({
            type: 'SEND_LOOPER_COMMAND',
            payload: {'command': command}
        })
    }

    const recordTimeUpdated = e => {
        setRecordTime(e.target.value);
    }
    
    const sendRecordTime = () => {
        dispatch({
            type: 'SEND_RECORD_TIME',
            payload: {value: recordTime}
        });
    }

    const styles = {
        margin: 5,
    };

    return (
        <Grid item lg={12} sx={{ mt: 10 }}>
            <Paper>
                <Button variant="outlined" sx={styles} 
                        onClick={() => sendCommand('random')}>
                    Shuffle
                </Button>
                <Button variant="outlined" sx={styles}
                        onClick={() => sendCommand('play')}>
                    Play/Stop
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
                        onClick={() => sendCommand('save')}>
                    Save
                </Button>
                <Button variant="outlined" sx={styles}
                        onClick={() => sendCommand('send')}>
                    Send
                </Button>
            </Paper>
            <Paper>
                <TextField 
                    id="recordtime" 
                    label="Record Time" 
                    variant="outlined" 
                    onChange={recordTimeUpdated}
                /> 
                <Button variant="outlined" sx={styles}
                    onClick={() => sendRecordTime()}>
                    Set 
                </Button>
            </Paper>
        </Grid>
    )

}

export default AudioControls;
