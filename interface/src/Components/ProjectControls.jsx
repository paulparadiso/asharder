import React, { useContext, useState } from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider'
import { ClassNames } from '@emotion/react';

const ProjectControls = props => {

    const [state, dispatch] = useContext(AudioParameterContext);
    const [name, setName] = useState('');

    const textFieldUpdated = e => {
        setName(e.target.value)
    }

    const setProjectName = () => {
        dispatch({
            type: 'SET_PROJECT_NAME',
            payload: {
                value: name
            }
        })
    }

    return (
        <Grid item lg={12}>
                <TextField
                    id="project-name"
                    label="Project Name"
                    defaultValue=""
                    onChange={textFieldUpdated}
                />
                <Button variant="outlined" onClick={setProjectName}>
                    set
                </Button>
        </Grid>
    )

}

export default ProjectControls;