import { useEffect, useRef, useMemo } from 'react';
import * as d3 from 'd3';
import { format, parseISO } from 'date-fns';

export default function IncomeExpenseChart({ transactions }) {
  const svgRef = useRef();

  const chartData = useMemo(() => {
    const dataMap = {};

    transactions.forEach((txn) => {
      const date = format(parseISO(txn.date), 'MMM dd');
      if (!dataMap[date]) {
        dataMap[date] = { date, income: 0, expense: 0 };
      }
      if (txn.type === 'income') {
        dataMap[date].income += txn.amount;
      } else {
        dataMap[date].expense += txn.amount;
      }
    });

    return Object.values(dataMap).sort((a, b) => new Date(a.date) - new Date(b.date));
  }, [transactions]);

  useEffect(() => {
    if (chartData.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const width = 500 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const g = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
      .domain(chartData.map(d => d.date))
      .range([0, width])
      .padding(0.3);

    const y = d3.scaleLinear()
      .domain([0, d3.max(chartData, d => Math.max(d.income, d.expense))])
      .nice()
      .range([height, 0]);

    // X axis
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('transform', 'rotate(-45)')
      .style('text-anchor', 'end')
      .style('font-size', '10px');

    // Y axis
    g.append('g')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d => `₹${d}`))
      .style('font-size', '11px');

    // Income bars
    g.selectAll('.bar-income')
      .data(chartData)
      .enter()
      .append('rect')
      .attr('class', 'bar-income')
      .attr('x', d => x(d.date))
      .attr('y', d => y(d.income))
      .attr('width', x.bandwidth() / 2)
      .attr('height', d => height - y(d.income))
      .attr('fill', '#10b981')
      .style('opacity', 0.8);

    // Expense bars
    g.selectAll('.bar-expense')
      .data(chartData)
      .enter()
      .append('rect')
      .attr('class', 'bar-expense')
      .attr('x', d => x(d.date) + x.bandwidth() / 2)
      .attr('y', d => y(d.expense))
      .attr('width', x.bandwidth() / 2)
      .attr('height', d => height - y(d.expense))
      .attr('fill', '#ef4444')
      .style('opacity', 0.8);

  }, [chartData]);

  if (chartData.length === 0) {
    return null;
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Income vs Expenses</h3>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
        <svg ref={svgRef}></svg>
        <div style={{ marginTop: '1rem', display: 'flex', gap: '1.5rem', fontSize: '0.875rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '16px', height: '16px', backgroundColor: '#10b981', borderRadius: '2px' }} />
            <span>Income</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '16px', height: '16px', backgroundColor: '#ef4444', borderRadius: '2px' }} />
            <span>Expenses</span>
          </div>
        </div>
      </div>
    </div>
  );
}
