import React, { useEffect, useState, createContext, useRef } from 'react';
import axios from 'axios';

export const FileContext = createContext();

const FileProvider = ({ children }) => {
 
    const [files, setFiles] = useState({});
    const filesRef = useRef({});

    useEffect(() => {
        setInterval(() => {
            axios.get('http://localhost:5000/files').then(response => {
                if(JSON.stringify(filesRef.current) !== JSON.stringify(response.data)) {
                    console.log(JSON.stringify(response.data));
                    //console.log(JSON.stringify(files));
                    //setFiles(response.data);
                    filesRef.current = response.data;
                    setFiles(response.data);
                    setTimeout(() => console.log(files), 500);
                    //console.log(response.data);
                }
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