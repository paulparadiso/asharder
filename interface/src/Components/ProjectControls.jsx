import React, { useContext, useState, useEffect } from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider'
import { ClassNames } from '@emotion/react';

const ProjectControls = props => {

    const [state, dispatch] = useContext(AudioParameterContext);
    const [name, setName] = useState('UNSORTED');

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
    
    useEffect(() => {
        setProjectName();
    }, [])

    return (
        <Grid item lg={12}>
                <TextField
                    id="project-name"
                    label="Project Name"
                    defaultValue="UNSORTED"
                    onChange={textFieldUpdated}
                />
                <Button variant="outlined" onClick={setProjectName}>
                    set
                </Button>
        </Grid>
    )

}

export default ProjectControls;
