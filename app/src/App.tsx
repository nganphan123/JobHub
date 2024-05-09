import * as React from 'react';
import './App.css';
import { Container } from '@mui/material';
import { LocationOn, SpaceDashboard, Work } from '@mui/icons-material';
import TextInput from './components/SearchInput';
import Selection from './components/Selection';

const platforms = ['Linkedin', 'Indeed'];

function App() {
  return (
    <React.Fragment>
      <Container style={{ marginTop: '10px' }}>
        <TextInput label={'Job Title'} icon={<Work />} />
        <TextInput label={'Location'} icon={<LocationOn />} />
        <Selection
          options={platforms}
          icon={<SpaceDashboard />}
          label="Platform"
          labelId="platform-select-label"
        />
      </Container>
    </React.Fragment>
  );
}

export default App;
