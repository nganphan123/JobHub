import Checkbox from '@mui/material/Checkbox';
import {
  FormControl,
  InputAdornment,
  InputLabel,
  ListItemText,
  MenuItem,
  OutlinedInput,
  Select,
  SelectChangeEvent
} from '@mui/material';
import { ReactNode, useState } from 'react';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250
    }
  }
};

interface SelectionProps {
  options: string[];
  icon: ReactNode;
  label: string;
  labelId: string;
  customStyle?: React.CSSProperties;
  // onChange:
}

export default function Selection({
  options,
  icon,
  label,
  labelId,
  customStyle
}: SelectionProps) {
  const [selected, setSelected] = useState<string[]>([]);
  const handleChange = (event: SelectChangeEvent<typeof selected>) => {
    const {
      target: { value }
    } = event;
    setSelected(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value
    );
  };
  return (
    <FormControl style={customStyle}>
      <InputLabel id={labelId}>{label}</InputLabel>
      <Select
        multiple
        value={selected}
        onChange={handleChange}
        renderValue={(values) => values.join(', ')}
        MenuProps={MenuProps}
        startAdornment={
          <InputAdornment position="start">{icon}</InputAdornment>
        }
        variant="outlined"
        labelId={labelId}
        input={<OutlinedInput label={label} />}
      >
        {options.map((opt) => (
          <MenuItem key={opt} value={opt}>
            <Checkbox checked={selected.indexOf(opt) > -1} />
            <ListItemText primary={opt} />
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
