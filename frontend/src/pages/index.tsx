import React, { useEffect, useState } from 'react';
import { Container, Typography } from '@mui/material';
import TotalTrials from '../components/TotalTrials';
import ConditionsPieChart from '../components/ConditionsPieChart';
import SponsorsBarChart from '../components/SponsorsBarChart';
import { fetchTotalTrials, fetchConditionsData, fetchSponsorsData } from '../api';

const Dashboard: React.FC = () => {
  const [totalTrials, setTotalTrials] = useState({ clinicalTrialsGov: 0, eudraCT: 0 });
  const [conditionsData, setConditionsData] = useState([]);
  const [sponsorsData, setSponsorsData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const totalTrialsData = await fetchTotalTrials();
        setTotalTrials(totalTrialsData);

        const conditions = await fetchConditionsData();
        setConditionsData(conditions);

        const sponsors = await fetchSponsorsData();
        setSponsorsData(sponsors);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <Container className="dark:bg-gray-900 dark:text-white">
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