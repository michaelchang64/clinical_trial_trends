import React from 'react';
import CustomTooltip from './CustomTooltip';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell } from 'recharts';

interface DataItem {
  name: string;
  value: number;
}

interface SponsorsBarChartProps {
  data: DataItem[];
}

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042'];

const SponsorsBarChart: React.FC<SponsorsBarChartProps> = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#ccc" />
        <XAxis dataKey="name" stroke="#ccc" tick={{ fontSize: 12 }} />
        <YAxis stroke="#ccc" />
        <Tooltip content={<CustomTooltip unit="trials" />} />
        <Bar dataKey="value">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default SponsorsBarChart;