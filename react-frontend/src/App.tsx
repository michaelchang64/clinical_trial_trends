import React, { useEffect, useState } from 'react';
import { Container, Grid, Box, Typography, Select, MenuItem } from '@mui/material';
import TotalTrials from './components/TotalTrials';
import ConditionsPieChart from './components/ConditionsPieChart';
import SponsorsBarChart from './components/SponsorsBarChart';
import { fetchTotalTrials, fetchConditionsData, fetchSponsorsData } from './api';

const App: React.FC = () => {
  const [totalTrials, setTotalTrials] = useState({ clinicalTrialsGov: 0, eudraCT: 0 });
  const [conditionsData, setConditionsData] = useState([]);
  const [sponsorsData, setSponsorsData] = useState([]);
  const [conditionsLimit, setConditionsLimit] = useState(10);
  const [sponsorsLimit, setSponsorsLimit] = useState(10);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const totalTrialsData = await fetchTotalTrials();
        setTotalTrials(totalTrialsData);

        const conditions = await fetchConditionsData();
        setConditionsData(conditions.slice(0, conditionsLimit));

        const sponsors = await fetchSponsorsData();
        setSponsorsData(sponsors.slice(0, sponsorsLimit));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [conditionsLimit, sponsorsLimit]);

  return (
    <Container maxWidth="lg" className="dark:bg-gray-900 dark:text-white min-h-screen p-4">
      <Typography variant="h3" align="center" gutterBottom>
        Clinical Trials Dashboard
      </Typography>
      <Grid container spacing={4} justifyContent="center">
        <Grid item xs={12} md={4}>
          <TotalTrials clinicalTrialsGov={totalTrials.clinicalTrialsGov} eudraCT={totalTrials.eudraCT} />
        </Grid>
        <Grid item xs={12} md={8}>
          <Box className="bg-gray-800 p-4 rounded-lg shadow-md">
            <ConditionsPieChart data={conditionsData} />
            <Typography variant="body1" className="text-white mt-2">
              Conditions Limit:
            </Typography>
            <Select
              value={conditionsLimit}
              onChange={(e) => setConditionsLimit(Number(e.target.value))}
              className="bg-gray-800 text-white rounded"
            >
              <MenuItem value={5}>5</MenuItem>
              <MenuItem value={10}>10</MenuItem>
              <MenuItem value={15}>15</MenuItem>
            </Select>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box className="bg-gray-800 p-4 rounded-lg shadow-md">
            <SponsorsBarChart data={sponsorsData} />
            <Typography variant="body1" className="text-white mt-2">
              Sponsors Limit:
            </Typography>
            <Select
              value={sponsorsLimit}
              onChange={(e) => setSponsorsLimit(Number(e.target.value))}
              className="bg-gray-800 text-white rounded"
            >
              <MenuItem value={5}>5</MenuItem>
              <MenuItem value={10}>10</MenuItem>
              <MenuItem value={15}>15</MenuItem>
            </Select>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default App;