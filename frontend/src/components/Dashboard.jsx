import { useMemo } from 'react';
import SpendingChart from './SpendingChart';
import IncomeExpenseChart from './IncomeExpenseChart';

export default function Dashboard({ transactions }) {
  const stats = useMemo(() => {
    let totalIncome = 0;
    let totalExpense = 0;

    transactions.forEach((txn) => {
      if (txn.type === 'income') {
        totalIncome += txn.amount;
      } else {
        totalExpense += txn.amount;
      }
    });

    const netSavings = totalIncome - totalExpense;
    const savingsRate = totalIncome > 0 ? (netSavings / totalIncome) * 100 : 0;

    return {
      totalIncome,
      totalExpense,
      netSavings,
      savingsRate,
    };
  }, [transactions]);

  return (
    <div>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Income</div>
          <div className="stat-value positive">
            ₹{stats.totalIncome.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Total Expenses</div>
          <div className="stat-value negative">
            ₹{stats.totalExpense.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Net Savings</div>
          <div className={`stat-value ${stats.netSavings >= 0 ? 'positive' : 'negative'}`}>
            ₹{stats.netSavings.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Savings Rate</div>
          <div className={`stat-value ${stats.savingsRate >= 20 ? 'positive' : ''}`}>
            {stats.savingsRate.toFixed(1)}%
          </div>
        </div>
      </div>

      {transactions.length > 0 && (
        <div className="grid grid-2">
          <IncomeExpenseChart transactions={transactions} />
          <SpendingChart transactions={transactions} />
        </div>
      )}
    </div>
  );
}
