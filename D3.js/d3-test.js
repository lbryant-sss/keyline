// Define margins
const margin = {
    top: 70,
    right: 30,
    bottom: 40,
    left: 80
};

// Calculate width and height based on margins
const width = 500 - margin.left - margin.right;
const height = 200 - margin.top - margin.bottom;

// Create SVG element
const svg = d3.select("#chart-container")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g") // Append a 'g' element for grouping to apply margins
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Optionally, add a title
svg.append("text")
    .attr("x", width / 2)
    .attr("y", -margin.top / 2)
    .attr("text-anchor", "middle")
    .style("font-size", "1.5em")
    .text("Your Chart Title");

// Example data (replace with your actual data loading)
const data = [
    { date: "2024-01-01", value: 10 },
    { date: "2024-02-01", value: 20 },
    { date: "2024-03-01", value: 15 },
    // Add more data points as needed
];

// Parse date format
const parseDate = d3.timeParse("%Y-%m-%d");

// Set up scales
const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => parseDate(d.date)))
    .range([0, width]);

const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([height, 0]);

// Optionally, add axis
const xAxis = d3.axisBottom(xScale);
const yAxis = d3.axisLeft(yScale);

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", `translate(0, ${height})`)
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

// Example of plotting data points
svg.selectAll(".dot")
    .data(data)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("cx", d => xScale(parseDate(d.date)))
    .attr("cy", d => yScale(d.value))
    .attr("r", 5);
