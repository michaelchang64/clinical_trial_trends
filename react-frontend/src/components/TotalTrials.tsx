import React from 'react';
import { Box, Typography } from '@mui/material';

interface TotalTrialsProps {
  clinicalTrialsGov: number;
  eudraCT: number;
}

const TotalTrials: React.FC<TotalTrialsProps> = ({ clinicalTrialsGov, eudraCT }) => {
  return (
    <Box className="bg-gray-800 p-4 rounded-lg shadow-md mb-4 flex justify-around">
      <Box textAlign="center">
        <Typography variant="h6" className="text-white">ClinicalTrials.gov</Typography>
        <Typography variant="h4" className="text-white">{clinicalTrialsGov}</Typography>
      </Box>
      <Box textAlign="center">
        <Typography variant="h6" className="text-white">EudraCT</Typography>
        <Typography variant="h4" className="text-white">{eudraCT}</Typography>
      </Box>
    </Box>
  );
};

export default TotalTrials;