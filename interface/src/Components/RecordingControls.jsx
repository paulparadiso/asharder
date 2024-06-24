import React, { useContext } from 'react';
import Grid from '@mui/material/Grid';
import Slider from '@mui/material/Slider';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider'
import axios from 'axios'

const RecordingControls = props => {

    const [state, dispatch] = useContext(AudioParameterContext)

    const handleSlider = (e, value) => {
        dispatch({
            type: 'SET_INPUT_LEVEL',
            payload: {
                'target': e.target.name,
                'value': value
            }
        });
    }

    const sliderStyles = {
        height: '50vh',
        marginRight: '1.3vw'
    }

    return (
        <Grid item lg={12}>
            <Slider
                defaultValue={0}
                valueLabelDisplay="auto"
                name="loopLevel"
                onChange={handleSlider}
                label="Loop Level"
                orientation="vertical"
                style={sliderStyles}
            >

            </Slider>
            <Slider
                defaultValue={0}
                valueLabelDisplay="auto"
                name="inputLevel1"
                onChange={handleSlider}
                label="Input Level 1"
                orientation="vertical"
                style={sliderStyles}
            >

            </Slider>
            <Slider
                defaultValue={0}
                valueLabelDisplay="auto"
                name="inputLevel2"
                onChange={handleSlider}
                label="Input Level 2"
                orientation="vertical"
                style={sliderStyles}
            >

            </Slider>
        </Grid>
    )

}

export default RecordingControls;