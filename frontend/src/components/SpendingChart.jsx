import { useEffect, useRef, useMemo } from 'react';
import * as d3 from 'd3';

export default function SpendingChart({ transactions }) {
  const svgRef = useRef();

  const expenseData = useMemo(() => {
    const categoryTotals = {};
    
    transactions
      .filter((txn) => txn.type === 'expense')
      .forEach((txn) => {
        const category = txn.category || 'Other';
        categoryTotals[category] = (categoryTotals[category] || 0) + txn.amount;
      });

    return Object.entries(categoryTotals)
      .map(([category, amount]) => ({ category, amount }))
      .sort((a, b) => b.amount - a.amount)
      .slice(0, 8); // Top 8 categories
  }, [transactions]);

  useEffect(() => {
    if (expenseData.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = 400;
    const height = 300;
    const radius = Math.min(width, height) / 2;

    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const color = d3.scaleOrdinal()
      .domain(expenseData.map(d => d.category))
      .range(d3.schemeSet3);

    const pie = d3.pie().value(d => d.amount);
    const arc = d3.arc().innerRadius(radius * 0.5).outerRadius(radius * 0.8);

    const arcs = g
      .selectAll('.arc')
      .data(pie(expenseData))
      .enter()
      .append('g')
      .attr('class', 'arc');

    arcs
      .append('path')
      .attr('d', arc)
      .attr('fill', d => color(d.data.category))
      .attr('stroke', 'white')
      .attr('stroke-width', 2)
      .style('opacity', 0.9)
      .on('mouseover', function() {
        d3.select(this).style('opacity', 1);
      })
      .on('mouseout', function() {
        d3.select(this).style('opacity', 0.9);
      });

    arcs
      .append('text')
      .attr('transform', d => `translate(${arc.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .attr('font-size', '11px')
      .attr('fill', '#333')
      .attr('font-weight', '600')
      .text(d => {
        const percentage = (d.data.amount / d3.sum(expenseData, e => e.amount)) * 100;
        return percentage > 5 ? `${percentage.toFixed(0)}%` : '';
      });

  }, [expenseData]);

  if (expenseData.length === 0) {
    return null;
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Spending by Category</h3>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
        <svg ref={svgRef}></svg>
        <div style={{ marginTop: '1rem', display: 'flex', flexWrap: 'wrap', gap: '0.75rem', justifyContent: 'center' }}>
          {expenseData.map((item, index) => (
            <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem' }}>
              <div
                style={{
                  width: '12px',
                  height: '12px',
                  borderRadius: '2px',
                  backgroundColor: d3.schemeSet3[index % d3.schemeSet3.length],
                }}
              />
              <span>{item.category}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
