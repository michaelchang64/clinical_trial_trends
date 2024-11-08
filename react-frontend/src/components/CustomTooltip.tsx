import React from "react";

interface CustomTooltipProps {
  active?: boolean;
  payload?: { value: number }[];
  label?: string;
  unit?: string;
}

const CustomTooltip: React.FC<CustomTooltipProps> = ({
  active,
  payload,
  label,
  unit,
}) => {
  if (active && payload && payload.length) {
    let template: string = '';
    if (label) {
        template = `${label} : ${payload[0].value} ${unit}`
    } else {
        template = `${payload[0].value} ${unit}`
    }
    return (
      <div className="transition delay-150 ease-in-out bg-gray-700 bg-opacity-70 text-white p-2 rounded-md">
        <p className="label">{template}</p>
      </div>
    );
  }
  return null;
};

export default CustomTooltip;
