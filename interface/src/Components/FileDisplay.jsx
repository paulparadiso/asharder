import React, { useContext, useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Button from '@mui/material/Button';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider';
import { FileContext } from '../Contexts/FileProvider';

const FileDisplay = props => {

    const [state, dispatch] = useContext(AudioParameterContext);
    const files = useContext(FileContext);
    const [rows, setRows] = useState([]);

    const handlePlayClick = (e, cellValues) => {
        //console.log(cellValues.row.path)
        dispatch({
            type: 'PLAY_AUDIO_FILE',
            payload: {
                path: cellValues.row.path
            }
        })
    }

    const columns = [
        {
            field: 'id',
            headerName: 'ID',
            width: 10,
            editable: false,
        },
        {
            field: 'name',
            headerName: 'NAME',
            width: 50,
            editable: true,
        },
        {
            field: 'play',
            sortable: false,
            renderCell: (cellValues) => {
                return (
                    <Button
                        variant="outlined"
                        color="primary"
                        onClick={e => {
                            handlePlayClick(e, cellValues);
                        }}
                    >play</Button>
                )
            }
        }
    ]

    useEffect(() => {
        console.log(state.currentProjectName);
        console.log(files[0]);
        if(files[0][state.currentProjectName]) {
            setRows(files[0][state.currentProjectName]);
        } else {
            setRows([]);
        }
    }, [state.currentProjectName]);

    return (
        <>  
            <DataGrid
                rows={rows}
                columns={columns}
                getRowId={row => row.id}
                initialState={{
                    pagination: {
                        paginationModel: {
                            pageSize: 5
                        }
                    }
                }}
                pageSizeOptions={[5]}
                disableRowSelectionOnClick
            >

            </DataGrid>
        </>
    )
}

export default FileDisplay;