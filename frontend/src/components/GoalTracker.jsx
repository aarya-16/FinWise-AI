import { useState } from 'react';
import { createGoal } from '../services/api';

export default function GoalTracker({ goals, onGoalAdded }) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    target_amount: '',
    target_date: '',
    current_amount: 0,
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const goalData = {
        ...formData,
        target_amount: parseFloat(formData.target_amount),
        current_amount: parseFloat(formData.current_amount) || 0,
        target_date: new Date(formData.target_date).toISOString(),
      };

      await createGoal(goalData);
      setFormData({ title: '', target_amount: '', target_date: '', current_amount: 0 });
      setShowForm(false);
      onGoalAdded();
    } catch (error) {
      alert('Error creating goal: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Savings Goals</h2>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
          style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
        >
          {showForm ? 'Cancel' : '+ New Goal'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} style={{ marginBottom: '1.5rem' }}>
          <div className="form-group">
            <label className="form-label">Goal Title</label>
            <input
              type="text"
              className="form-input"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g., Emergency Fund"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Target Amount (₹)</label>
            <input
              type="number"
              className="form-input"
              value={formData.target_amount}
              onChange={(e) => setFormData({ ...formData, target_amount: e.target.value })}
              placeholder="10000"
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Target Date</label>
            <input
              type="date"
              className="form-input"
              value={formData.target_date}
              onChange={(e) => setFormData({ ...formData, target_date: e.target.value })}
              required
            />
          </div>

          <button type="submit" className="btn btn-success" disabled={loading} style={{ width: '100%' }}>
            {loading ? 'Creating...' : 'Create Goal'}
          </button>
        </form>
      )}

      {goals.length === 0 ? (
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>
          No goals yet. Create your first savings goal!
        </p>
      ) : (
        <div>
          {goals.map((goal) => {
            const progress = (goal.current_amount / goal.target_amount) * 100;
            return (
              <div key={goal._id} style={{ marginBottom: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ fontWeight: '600' }}>{goal.title}</span>
                  <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    ₹{goal.current_amount.toLocaleString('en-IN')} / ₹{goal.target_amount.toLocaleString('en-IN')}
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: 'var(--border-color)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${Math.min(progress, 100)}%`,
                      height: '100%',
                      backgroundColor: 'var(--success-color)',
                      transition: 'width 0.3s',
                    }}
                  />
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                  {progress.toFixed(1)}% complete
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
