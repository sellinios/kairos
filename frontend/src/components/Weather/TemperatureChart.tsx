// src/components/Weather/TemperatureChart.tsx
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface TemperatureChartProps {
  data: { date: string; temperature: number }[];
}

const TemperatureChart: React.FC<TemperatureChartProps> = ({ data }) => {
  const svgRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = 600;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };

    // Clear previous chart
    svg.selectAll('*').remove();

    // Set up scales
    const x = d3.scaleBand()
      .domain(data.map(d => d.date))
      .range([margin.left, width - margin.right])
      .padding(0.1);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.temperature) || 0])
      .nice()
      .range([height - margin.bottom, margin.top]);

    // Set up axes
    const xAxis = (g: any) => g
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickSizeOuter(0));

    const yAxis = (g: any) => g
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .call((g: any) => g.select('.domain').remove());

    // Draw the axes
    svg.append('g').call(xAxis);
    svg.append('g').call(yAxis);

    // Draw the line
    const line = d3.line<{ date: string; temperature: number }>()
      .x(d => x(d.date)!)
      .y(d => y(d.temperature));

    svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 1.5)
      .attr('d', line);

  }, [data]);

  return <svg ref={svgRef} width={600} height={300} />;
};

export default TemperatureChart;
