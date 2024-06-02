import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import WeatherIcon from './WeatherIcon';

const D3Chart = ({ data, height = 400 }) => {
  const ref = useRef();

  useEffect(() => {
    const svg = d3.select(ref.current);
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    let width = ref.current.parentElement.offsetWidth;

    const renderChart = () => {
      width = ref.current.parentElement.offsetWidth;

      svg.attr('width', width)
        .attr('height', height)
        .attr('viewBox', `0 0 ${width} ${height}`)
        .style('max-width', '100%')
        .style('height', 'auto');

      const x = d3.scaleTime()
        .domain(d3.extent(data, d => new Date(d.date)))
        .range([margin.left, width - margin.right]);

      const y = d3.scaleLinear()
        .domain([d3.min(data, d => d.value) - 1, d3.max(data, d => d.value) + 1])
        .nice()
        .range([height - margin.bottom, margin.top]);

      const xAxis = g => g
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
        .call(g => g.selectAll("text").attr("fill", "white"))
        .call(g => g.selectAll("line").attr("stroke", "white"))
        .call(g => g.select(".domain").attr("stroke", "white"));

      const yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .call(g => g.selectAll("text").attr("fill", "white"))
        .call(g => g.selectAll("line").attr("stroke", "white"))
        .call(g => g.select(".domain").attr("stroke", "white"));

      const line = d3.line()
        .defined(d => !isNaN(d.value))
        .x(d => x(new Date(d.date)))
        .y(d => y(d.value));

      svg.selectAll("*").remove();

      svg.append("g")
        .call(xAxis);

      svg.append("g")
        .call(yAxis);

      svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "white")  // Changed to white
        .attr("stroke-width", 1.5)
        .attr("d", line);

      // Add icons to the chart
      const iconSize = 20;  // Adjust the icon size as needed

      // Append icons using React components
      const iconSelection = svg.selectAll(".weather-icon")
        .data(data)
        .enter()
        .append("foreignObject")
        .attr("x", d => x(new Date(d.date)) - iconSize / 2)
        .attr("y", d => y(d.value) - iconSize / 2)
        .attr("width", iconSize)
        .attr("height", iconSize)
        .classed("weather-icon", true);

      iconSelection.append("xhtml:div")
        .html(d => {
          const state = d.state; // Assuming each data point has a 'state' property for the weather state
          return `<div style="width: ${iconSize}px; height: ${iconSize}px;">
                    <WeatherIcon state="${state}" width=${iconSize} height=${iconSize} />
                  </div>`;
        });
    };

    renderChart();

    const resizeObserver = new ResizeObserver(() => {
      renderChart();
    });

    resizeObserver.observe(ref.current.parentElement);

    return () => resizeObserver.unobserve(ref.current.parentElement);
  }, [data, height]);

  return (
    <svg ref={ref}></svg>
  );
};

export default D3Chart;
