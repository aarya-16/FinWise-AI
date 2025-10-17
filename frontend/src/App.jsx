import { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import TransactionForm from './components/TransactionForm';
import TransactionList from './components/TransactionList';
import InsightsBanner from './components/InsightsBanner';
import GoalTracker from './components/GoalTracker';
import { getTransactions, getInsights, getGoals } from './services/api';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [insights, setInsights] = useState(null);
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [txnData, goalsData] = await Promise.all([
        getTransactions(),
        getGoals(),
      ]);
      
      setTransactions(txnData.transactions || []);
      setGoals(goalsData.goals || []);
      
      // Fetch insights only if transactions exist
      if (txnData.transactions && txnData.transactions.length > 0) {
        try {
          const insightsData = await getInsights();
          setInsights(insightsData);
        } catch (error) {
          console.error('Error fetching insights:', error);
        }
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTransactionAdded = () => {
    fetchData();
  };

  const handleGoalAdded = () => {
    fetchData();
  };

  if (loading) {
    return (
      <>
        <Header />
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading your financial data...</p>
        </div>
      </>
    );
  }

  return (
    <div className="app">
      <Header />
      
      <div className="container">
        {insights && <InsightsBanner insights={insights} />}
        
        <Dashboard transactions={transactions} />
        
        <div className="grid grid-2">
          <TransactionForm onTransactionAdded={handleTransactionAdded} />
          <GoalTracker goals={goals} onGoalAdded={handleGoalAdded} />
        </div>
        
        <TransactionList 
          transactions={transactions} 
          onTransactionDeleted={fetchData}
        />
      </div>
    </div>
  );
}

export default App;
