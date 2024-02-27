import React, { createContext, useReducer } from 'react';

export const GlobalContext = createContext();

const reducer = (action, payload) => {
    switch (action.type) {
        case 'SET_GLOBAL':
            return {...state,
                    [payload.data.key]: [payload.data.value]}
        default:
            break;
    }
}

const initialState = {}

const GlobalProvider = ( {children}) => {

    const [state, dispatch] = useReducer(reducer, initialState);

    return (
        <GlobalContext.Provider value={[state, dispatch]}>
            { children }
        </GlobalContext.Provider>
    )

}

export default GlobalProvider;