import { InputAdornment, TextField } from '@mui/material';
import { ReactNode } from 'react';

interface TextInputProps {
  label: string;
  icon: ReactNode;
}
export default function TextInput({ label, icon }: TextInputProps) {
  return (
    <TextField
      label={label}
      variant="outlined"
      InputProps={{
        startAdornment: <InputAdornment position="start">{icon}</InputAdornment>
      }}
    ></TextField>
  );
}
