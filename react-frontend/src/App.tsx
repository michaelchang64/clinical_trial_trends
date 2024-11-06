import React, { useEffect, useState } from 'react';
import { Container, Grid, Box, Typography, Select, MenuItem, FormControl } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import TotalTrials from './components/TotalTrials';
import ConditionsPieChart from './components/ConditionsPieChart';
import SponsorsBarChart from './components/SponsorsBarChart';
import { fetchTotalTrials, fetchConditionsData, fetchSponsorsData } from './api';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

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
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
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
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h5" className="text-white">
                Conditions Distribution
              </Typography>
              <FormControl variant="outlined" size="small">
                <Select
                  value={conditionsLimit}
                  onChange={(e) => setConditionsLimit(Number(e.target.value))}
                  className="bg-gray-800 text-white rounded"
                >
                  <MenuItem value={5}>5</MenuItem>
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={15}>15</MenuItem>
                  <MenuItem value={20}>20</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <ConditionsPieChart data={conditionsData} />
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box className="bg-gray-800 p-4 rounded-lg shadow-md">
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h5" className="text-white">
                Sponsors Distribution
              </Typography>
              <FormControl variant="outlined" size="small">
                <Select
                  value={sponsorsLimit}
                  onChange={(e) => setSponsorsLimit(Number(e.target.value))}
                  className="bg-gray-800 text-white rounded"
                >
                  <MenuItem value={5}>5</MenuItem>
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={15}>15</MenuItem>
                  <MenuItem value={20}>20</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <SponsorsBarChart data={sponsorsData} />
          </Box>
        </Grid>
      </Grid>
    </Container>
    </ThemeProvider>
  );
};

export default App;