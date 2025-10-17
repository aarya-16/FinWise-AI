import { useState } from 'react';
import { createTransaction, uploadTransactionsCSV } from '../services/api';

export default function TransactionForm({ onTransactionAdded }) {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    amount: '',
    type: 'expense',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const transactionData = {
        ...formData,
        date: new Date(formData.date).toISOString(),
        amount: parseFloat(formData.amount),
      };

      await createTransaction(transactionData);
      setMessage('✅ Transaction added successfully!');
      setFormData({
        date: new Date().toISOString().split('T')[0],
        amount: '',
        type: 'expense',
        description: '',
      });
      onTransactionAdded();
    } catch (error) {
      setMessage('❌ Error adding transaction: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setMessage('');

    try {
      const result = await uploadTransactionsCSV(file);
      setMessage(`✅ Uploaded ${result.transactions_added} transactions!`);
      onTransactionAdded();
    } catch (error) {
      setMessage('❌ Error uploading CSV: ' + error.message);
    } finally {
      setLoading(false);
      e.target.value = '';
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Add Transaction</h2>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Date</label>
          <input
            type="date"
            className="form-input"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Amount (₹)</label>
          <input
            type="number"
            className="form-input"
            value={formData.amount}
            onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
            placeholder="0.00"
            step="0.01"
            min="0"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Type</label>
          <select
            className="form-select"
            value={formData.type}
            onChange={(e) => setFormData({ ...formData, type: e.target.value })}
            required
          >
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Description</label>
          <input
            type="text"
            className="form-input"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="e.g., Freelance project, Food delivery"
            required
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%', marginBottom: '1rem' }}>
          {loading ? 'Adding...' : '➕ Add Transaction'}
        </button>
      </form>

      <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1rem', marginTop: '1rem' }}>
        <label className="form-label">Or upload CSV</label>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          disabled={loading}
          className="form-input"
        />
        <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
          CSV format: date,amount,type,description
        </p>
      </div>

      {message && (
        <div style={{ marginTop: '1rem', padding: '0.75rem', borderRadius: '8px', backgroundColor: message.includes('❌') ? '#fee2e2' : '#d1fae5' }}>
          {message}
        </div>
      )}
    </div>
  );
}
