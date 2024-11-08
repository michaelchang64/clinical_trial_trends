import React from 'react';
import CustomTooltip from './CustomTooltip';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ConditionsPieChartProps {
  data: { name: string; value: number }[];
}

const COLORS = [
  '#0088FE', // Blue
  '#00C49F', // Teal
  '#FFBB28', // Yellow
  '#FF8042', // Orange
  '#A28CFF', // Lavender
  '#FF6F91', // Pink
  '#FF6347', // Tomato
  '#32CD32', // Lime Green
  '#FFD700', // Gold
  '#8A2BE2', // Blue Violet
  '#FF4500', // Orange Red
  '#2E8B57', // Sea Green
  '#DA70D6', // Orchid
  '#4682B4', // Steel Blue
  '#9ACD32', // Yellow Green
  '#FF1493', // Deep Pink
  '#7FFF00'  // Chartreuse
];

const ConditionsPieChart: React.FC<ConditionsPieChartProps> = ({ data }) => {
  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-md">
      <ResponsiveContainer width="100%" height={260}>
        <PieChart width={900} >
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip unit="trials" />} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConditionsPieChart;