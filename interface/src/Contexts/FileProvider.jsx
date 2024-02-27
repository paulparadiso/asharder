import React, { useEffect, useState, createContext } from 'react';
import axios from 'axios';

export const FileContext = createContext();

const FileProvider = ({ children }) => {
 
    const [files, setFiles] = useState({});

    useEffect(() => {
        setInterval(() => {
            axios.get('http://localhost:5000/files').then(response => {
                setFiles(response.data);
            })
        }, 1000);
    }, []);

    return (
        <FileContext.Provider value={[files]}>
            {children}
        </FileContext.Provider>
    )

}

export default FileProvider;