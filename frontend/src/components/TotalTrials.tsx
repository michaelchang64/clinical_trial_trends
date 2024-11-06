import React from 'react';
import { Box, Typography } from '@mui/material';

interface TotalTrialsProps {
    clinicalTrialsGov: number;
    eudraCT: number;
}

const TotalTrials: React.FC<TotalTrialsProps> = ({ clinicalTrialsGov, eudraCT }) => {
    return (
    <Box display="flex" justifyContent="space-around" p={2}>
        <Box textAlign="center">
        <Typography variant="h6">ClinicalTrials.gov</Typography>
        <Typography variant="h4">{clinicalTrialsGov}</Typography>
        </Box>
        <Box textAlign="center">
        <Typography variant="h6">EudraCT</Typography>
        <Typography variant="h4">{eudraCT}</Typography>
        </Box>
    </Box>
    );
};

export default TotalTrials;