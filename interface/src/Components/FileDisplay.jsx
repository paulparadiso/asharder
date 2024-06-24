import React, { useContext, useEffect, useState, useRef } from 'react';
import { DataGrid, GridCellEditStartReasons } from '@mui/x-data-grid';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { AudioParameterContext } from '../Contexts/AudioParameterProvider';
import { FileContext } from '../Contexts/FileProvider';
import Checkbox from '@mui/material/Checkbox';

const FileDisplay = props => {

    const [state, dispatch] = useContext(AudioParameterContext);
    const files = useContext(FileContext);
    const [rows, setRows] = useState([]);

    let fileUpdates = useRef({});

    const saveUpdates = () => {
        console.log(fileUpdates.current);
        dispatch({
            type: 'UPDATE_FILES',
            payload: {
                data: fileUpdates.current
            }
        });
    }

    const handlePlayClick = (e, cellValues) => {
        //console.log(cellValues.row.path)
        dispatch({
            type: 'PLAY_AUDIO_FILE',
            payload: {
                path: cellValues.row.path
            }
        })
    }

    const handleSaveChangesClick = () => {
        saveUpdates();
    }

    const handleNameEditEnd = (cellData, oldCellData) => {
        const { id, name } = cellData;
        if (fileUpdates.current.hasOwnProperty(id)) {
            fileUpdates.current[id].name = name;
        } else {
            fileUpdates.current[id] = { name: name };
        }
        saveUpdates();
        return cellData;
    }

    const handleUploadChange = (e, cellValues) => {
        const value = e.target.checked;
        const id = cellValues.row.id;
        console.log(`Setting ${id} to ${value}`);
        if (fileUpdates.current.hasOwnProperty(id)) {
            console.log('appending')
            fileUpdates.current[id].upload = value
        } else {
            console.log('creating property');
            fileUpdates.current[id] = { upload: value };
        }
        saveUpdates();
        //cellValues.row.upload = !cellValues.row.upload;
    }

    const handleLoopAddChange = (e, cellValues) => {
        const value = e.target.checked;
        const id = cellValues.row.id;
        if (fileUpdates.current.hasOwnProperty(id)) {
            fileUpdates.current[id].addLoop = value
        } else {
            fileUpdates.current[id] = { addLoop: value };
        }
        saveUpdates();
    }

    const handleRowUpdateError = e => {
        console.log(e);
    }

    const DataGridTitle = () => {
        return (
            <Box style={{ width: "100%", display: "flex", justifyContent: "center", alignItems: "center" }}>
                <Typography variant="h6">{state.currentProjectName}</Typography>
            </Box>
        )
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
            width: 180,
            editable: true,
        },
        {
            field: 'PLAY',
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
        },
        {
            field: 'UPLOAD',
            sortable: false,
            renderCell: (cellValues) => {
                return (
                    <Checkbox
                        checked={cellValues.row.upload}
                        onChange={e => { 
                            handleUploadChange(e, cellValues); 
                            //checked = !cellValues.row.upload = cellValues.row.upload;
                        }}
                    />
                )
            }
        },
        {
            field: 'LOOP ADD',
            sortable: false,
            renderCell: (cellValues) => {
                return (
                    <Checkbox
                        onChange={e => { handleLoopAddChange(e, cellValues) }}
                    />
                )
            }
        },
    ]

    useEffect(() => {
        console.log(state.currentProjectName);
        console.log(files[0]);
        if (files[0][state.currentProjectName]) {
            setRows(files[0][state.currentProjectName]);
        } else {
            console.log('clearing rows');
            setRows([]);
        }
    }, [state.currentProjectName, files]);

    return (
        <>
            <DataGrid
                rows={rows}
                columns={columns}
                getRowId={row => row.id}
                processRowUpdate={handleNameEditEnd}
                onProcessRowUpdateError={handleRowUpdateError}
                initialState={{
                    pagination: {
                        paginationModel: {
                            pageSize: 5
                        }
                    }
                }}
                pageSizeOptions={[5]}
                disableRowSelectionOnClick
                slots={{
                    toolbar: DataGridTitle
                }}
                sx={{ mt: 4, height: '33vh' }}
            >

            </DataGrid>
            {/*
            <Button variant="outlined" sx={{ margin: 2, float: 'right' }}
                onClick={handleSaveChangesClick}
            >
                save changes
            </Button>
            */}
        </>
    )
}

export default FileDisplay;