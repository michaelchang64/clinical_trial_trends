import React from 'react';
import { Box, Typography } from '@mui/material';

interface TotalTrialsProps {
  clinicalTrialsGov: number;
  eudraCT: number;
}

const TotalTrials: React.FC<TotalTrialsProps> = ({ clinicalTrialsGov, eudraCT }) => {
  return (
    <Box
      className="bg-gray-800 p-4 rounded-lg shadow-md mb-4"
      display="flex"
      justifyContent="center"
      alignItems="center"
      height="100%" // Ensure the container takes full height
    >
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        mx={2}
      >
        <Typography variant="h5" className="text-white">ClinicalTrials.gov</Typography>
        <Typography variant="h3" className="text-white">{clinicalTrialsGov}</Typography>

        <Typography variant="h5" className="text-white">EudraCT</Typography>
        <Typography variant="h3" className="text-white">{eudraCT}</Typography>
      </Box>
    </Box>
  );
};

export default TotalTrials;