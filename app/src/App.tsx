import * as React from 'react';
import './App.css';
import { Autocomplete, Container, Stack, TextField } from '@mui/material';
import { LocationOn, SpaceDashboard, Work } from '@mui/icons-material';
import TextInput from './components/SearchInput';
import Selection from './components/Selection';
import skills from './SkillList';
import { useState } from 'react';

const platforms = ['Linkedin', 'Indeed'];

function App() {
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const handleSkillChange = (
    event: React.SyntheticEvent<Element, Event>,
    value: string[]
  ) => {
    setSelectedSkills(value);
  };
  return (
    <React.Fragment>
      <Stack style={{ marginTop: '10px' }} direction="row" spacing={2}>
        <TextInput
          label={'Job Title'}
          icon={<Work />}
          customStyle={{ width: '200px' }}
        />
        <TextInput
          label={'Location'}
          icon={<LocationOn />}
          customStyle={{ width: '200px' }}
        />
        <Selection
          options={platforms}
          icon={<SpaceDashboard />}
          label="Platform"
          labelId="platform-select-label"
          customStyle={{ width: '200px' }}
        />
        <Autocomplete
          disableCloseOnSelect
          sx={{ width: 350 }}
          multiple
          freeSolo
          options={skills}
          onChange={handleSkillChange}
          limitTags={3}
          renderInput={(params) => (
            <TextField {...params} variant="outlined" label="Skills" />
          )}
        />
      </Stack>
      <Stack direction="column"></Stack>
    </React.Fragment>
  );
}

export default App;
