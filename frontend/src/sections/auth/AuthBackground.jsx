// material-ui
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import SignalCellularAltIcon from '@mui/icons-material/SignalCellularAlt';

export default function AuthBackground() {
  const theme = useTheme();

  return (
    <Box
      sx={{
        position: 'absolute',
        filter: 'blur(30px)',
        zIndex: -1,
        bottom: 0,
        transform: 'inherit'
      }}
    >
      <SignalCellularAltIcon />

      <svg width="2500" height="600" viewBox="-20 -15 405 100">
        <rect x="10" y="60" width="10" height="20" fill="#1677ffe6" />
        <rect x="30" y="40" width="10" height="40" fill="#1677ffe6" />
        <rect x="50" y="20" width="10" height="60" fill="#1677ffe6" />
        <rect x="70" y="0" width="10" height="80" fill="#1677ffe6" />
      </svg>

    </Box>
  );
}
