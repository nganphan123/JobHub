import { InputAdornment, TextField } from '@mui/material';
import { ReactNode } from 'react';

interface TextInputProps {
  label: string;
  icon: ReactNode;
  customStyle?: React.CSSProperties;
}
export default function TextInput({
  label,
  icon,
  customStyle
}: TextInputProps) {
  return (
    <TextField
      style={customStyle}
      label={label}
      variant="outlined"
      InputProps={{
        startAdornment: <InputAdornment position="start">{icon}</InputAdornment>
      }}
    ></TextField>
  );
}
