import React, { useEffect, createContext, useReducer } from 'react';
import axios from 'axios';

export const AudioParameterContext = createContext();

const reducer = (state, action) => {
    switch(action.type) {
        case 'SET_INPUT_LEVEL':
            return {...state,
                [action.payload.target]: action.payload.value,
                nextProcess: {
                process: 'setLevel',
                data: {
                    target: action.payload.target,
                    value: action.payload.value
                }
            }};
        case 'SET_PROJECT_NAME':
            return {...state,
                currentProjectName: action.payload.value,
                nextProcess: {process: 'setProjectName', data:{name: action.payload.value}}
            };
        case 'PLAY_AUDIO_FILE':
            return {...state,
                    nextProcess: {process: 'playAudioFile', data: {path: action.payload.path}}
            }
        default:
            return state;
    }
}

const initialState = {
    loopLevel: 0.0,
    inputLevel1: 0.0,
    inputLevel2: 0.0,
    outputLevel1: 0.0,
    outputLevel2: 0.0,
    currentProjectName: '',
    nextProcess: null
}

const AudioParameterProvider = ({children}) => {

    const [state, dispatch] = useReducer(reducer, initialState);

    const setLevel = (target, value) => {
        axios.post('http://192.168.2.99:5000/setparam', 
                   JSON.stringify({param: target, value: value}),
                   {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                   }
                   ).then(res => {
                    console.log(res);
                   });
    }

    const setProjectName = name => {
        axios.post('http://localhost:5000/setparam',
                    JSON.stringify({param: 'projectName', value: name}),
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    ).then(res => {
                        console.log(res);
                    })
    }

    const playAudioFile = path => {
        axios.post('http://localhost:5000/play', 
                    JSON.stringify({path: path}),
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }).then(res => {
                        console.log(res);
                    }) 
        
    }

    useEffect(() => {
        if(state.nextProcess !== null) {
            if(state.nextProcess.process === 'setLevel') {
                setLevel(state.nextProcess.data['target'], state.nextProcess.data['value']);
            }
            if(state.nextProcess.process === 'setProjectName') {
                setProjectName(state.nextProcess.data['name']);
            }
            if(state.nextProcess.process === 'playAudioFile') {
                playAudioFile(state.nextProcess.data['path']);
            }
        }
    }, [state.nextProcess]);

    return (
        <AudioParameterContext.Provider value={[state, dispatch]}>
            {children}
        </AudioParameterContext.Provider>
    )

}

export default AudioParameterProvider;