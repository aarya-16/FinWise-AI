import { format } from 'date-fns';
import { deleteTransaction } from '../services/api';

export default function TransactionList({ transactions, onTransactionDeleted }) {
  const handleDelete = async (transactionId) => {
    if (!window.confirm('Are you sure you want to delete this transaction?')) {
      return;
    }

    try {
      await deleteTransaction(transactionId);
      onTransactionDeleted();
    } catch (error) {
      alert('Error deleting transaction: ' + error.message);
    }
  };

  if (transactions.length === 0) {
    return (
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Recent Transactions</h2>
        </div>
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>
          No transactions yet. Add your first transaction to get started!
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Recent Transactions</h2>
        <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          {transactions.length} total
        </span>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table className="transactions-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Category</th>
              <th>Type</th>
              <th>Amount</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((txn) => (
              <tr key={txn._id}>
                <td>{format(new Date(txn.date), 'MMM dd, yyyy')}</td>
                <td>{txn.description}</td>
                <td>
                  <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    {txn.category || 'Uncategorized'}
                  </span>
                </td>
                <td>
                  <span className={`badge badge-${txn.type}`}>
                    {txn.type}
                  </span>
                </td>
                <td style={{ fontWeight: '600', color: txn.type === 'income' ? 'var(--success-color)' : 'var(--text-primary)' }}>
                  ₹{txn.amount.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                </td>
                <td>
                  <button
                    onClick={() => handleDelete(txn._id)}
                    className="btn btn-secondary"
                    style={{ padding: '0.375rem 0.75rem', fontSize: '0.75rem' }}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
