import './App.css'
import Main from './Components/Main';
import AudioParameterProvider from './Contexts/AudioParameterProvider';
import FileProvider from './Contexts/FileProvider';

function App() {

    return (
        <AudioParameterProvider>
            <FileProvider>
                <Main />
            </FileProvider>
        </AudioParameterProvider>
    )
}

export default App
