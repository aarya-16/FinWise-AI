export default function InsightsBanner({ insights }) {
  if (!insights || (!insights.insights?.length && !insights.recommendations?.length)) {
    return null;
  }

  return (
    <div className="insight-banner">
      {insights.insights && insights.insights.length > 0 && (
        <>
          <h3 className="insight-title">
            🎯 Key Insights
          </h3>
          <ul className="insight-list">
            {insights.insights.map((insight, index) => (
              <li key={index} className="insight-item">
                {insight}
              </li>
            ))}
          </ul>
        </>
      )}

      {insights.recommendations && insights.recommendations.length > 0 && (
        <>
          <h3 className="insight-title" style={{ marginTop: '1.5rem' }}>
            💡 AI Recommendations
          </h3>
          <ul className="insight-list">
            {insights.recommendations.map((recommendation, index) => (
              <li key={index} className="insight-item">
                {recommendation}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
