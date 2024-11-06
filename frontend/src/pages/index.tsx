import React, { useEffect, useState } from 'react';
import { Container, Typography } from '@mui/material';
import TotalTrials from '../components/TotalTrials';
import ConditionsPieChart from '../components/ConditionsPieChart';
import SponsorsBarChart from '../components/SponsorsBarChart';

const Dashboard: React.FC = () => {
  const [totalTrials, setTotalTrials] = useState({ clinicalTrialsGov: 0, eudraCT: 0 });
  const [conditionsData, setConditionsData] = useState([]);
  const [sponsorsData, setSponsorsData] = useState([]);

  useEffect(() => {
    // Fetch total trials data
    fetch('/api/totalTrials')
      .then(response => response.json())
      .then(data => setTotalTrials(data));

    // Fetch conditions data
    fetch('/api/conditions')
      .then(response => response.json())
      .then(data => setConditionsData(data));

    // Fetch sponsors data
    fetch('/api/sponsors')
      .then(response => response.json())
      .then(data => setSponsorsData(data));
  }, []);

  return (
    <Container>
      <Typography variant="h3" gutterBottom>
        Clinical Trials Dashboard
      </Typography>
      <TotalTrials clinicalTrialsGov={totalTrials.clinicalTrialsGov} eudraCT={totalTrials.eudraCT} />
      <ConditionsPieChart data={conditionsData} />
      <SponsorsBarChart data={sponsorsData} />
    </Container>
  );
};

export default Dashboard;