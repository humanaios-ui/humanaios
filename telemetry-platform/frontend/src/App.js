import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [state, setState] = useState(null);
  const [learningState, setLearningState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [ecoAction, setEcoAction] = useState(null); // 'accepting', 'declining', or null
  const [ecoResult, setEcoResult] = useState(null); // success message or error

  useEffect(() => {
    const fetchState = async () => {
      try {
        const [stateRes, learningRes] = await Promise.all([
          fetch('http://localhost:3001/api/state'),
          fetch('http://localhost:3001/api/learning-state')
        ]);
        const stateData = await stateRes.json();
        const learningData = await learningRes.json();
        setState(stateData);
        setLearningState(learningData);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchState();
    const interval = setInterval(fetchState, 5000);
    return () => clearInterval(interval);
  }, []);

  // Handle ECO button actions
  const handleAcceptAll = async () => {
    setEcoAction('accepting');
    setEcoResult(null);
    try {
      const res = await fetch('http://localhost:3001/api/eco/accept-all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();
      setEcoResult({ success: true, message: data.message || 'Accepted all ECO proposals' });
      setEcoAction(null);
      // Refresh state after action
      setTimeout(() => {
        setState(prev => ({ ...prev, timestamp: new Date().toISOString() }));
      }, 1000);
    } catch (err) {
      setEcoResult({ success: false, message: err.message });
      setEcoAction(null);
    }
  };

  const handleDecline = async () => {
    setEcoAction('declining');
    setEcoResult(null);
    try {
      const reason = prompt('Reason for declining ECO proposals:');
      if (!reason) {
        setEcoAction(null);
        return;
      }
      const res = await fetch('http://localhost:3001/api/eco/decline-all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason })
      });
      const data = await res.json();
      setEcoResult({ success: true, message: data.message || 'Declined ECO proposals' });
      setEcoAction(null);
    } catch (err) {
      setEcoResult({ success: false, message: err.message });
      setEcoAction(null);
    }
  };

  const handleReview = () => {
    alert('Review functionality coming in Phase 2. For now, use the Cortex extension to review individual proposals.');
  };

  if (loading) return <div className="container"><p>Loading telemetry...</p></div>;
  if (error) return <div className="container error"><p>Error: {error}</p></div>;
  if (!state) return <div className="container"><p>No data</p></div>;

  return (
    <div className="container">
      <header>
        <h1>🚀 Phase 1 Orchestration Dashboard</h1>
        <p className="timestamp">Updated {new Date(state.timestamp).toLocaleTimeString()}</p>
      </header>

      {/* Alerts */}
      {state.alerts.length > 0 && (
        <section className="alerts">
          <h2>⚠️ Active Alerts</h2>
          {state.alerts.map((alert, i) => (
            <div key={i} className={`alert alert-${alert.level}`}>
              <strong>{alert.type.toUpperCase()}:</strong> {alert.message}
            </div>
          ))}
        </section>
      )}

      {/* Practice Grid */}
      <section className="practices">
        <h2>📊 Phase 1 Target Practices</h2>
        <div className="grid">
          {Object.values(state.practices).map(practice => (
            <div key={practice.name} className="practice-card">
              <div className="header">
                <h3>{practice.name}</h3>
                <span className="role">{practice.role}</span>
              </div>
              <div className="proposals">
                <h4>Proposals:</h4>
                {practice.proposals.length === 0 ? (
                  <p className="none">No proposals</p>
                ) : (
                  <ul>
                    {practice.proposals.map(p => (
                      <li key={p.id}>
                        <span className={`status status-${p.status}`}>{p.status}</span>
                        <span className="type">{p.type}</span>
                        <span className="count">{p.count}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Timeline */}
      <section className="timeline">
        <h2>📅 Phase 1 Milestones</h2>
        <div className="milestones">
          {state.timeline.map(m => (
            <div key={m.id} className="milestone">
              <span className="date">{m.date}</span>
              <span className="event">{m.event}</span>
              <span className={`status status-${m.status}`}>{m.status}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ECO Interface */}
      <section className="eco">
        <h2>🔒 ECO Decisions</h2>
        <div className="eco-buttons">
          <button
            className="btn btn-accept"
            onClick={handleAcceptAll}
            disabled={ecoAction === 'accepting'}
          >
            {ecoAction === 'accepting' ? '⏳ Accepting...' : '✅ Accept All ECO-Gated Proposals'}
          </button>
          <button
            className="btn btn-review"
            onClick={handleReview}
          >
            🔍 Review Individual Proposals
          </button>
          <button
            className="btn btn-decline"
            onClick={handleDecline}
            disabled={ecoAction === 'declining'}
          >
            {ecoAction === 'declining' ? '⏳ Declining...' : '❌ Decline & Rescope'}
          </button>
        </div>
        {ecoResult && (
          <div className={`eco-result ${ecoResult.success ? 'success' : 'error'}`}>
            {ecoResult.success ? '✅' : '❌'} {ecoResult.message}
          </div>
        )}
      </section>

      {/* Learning Curves */}
      {learningState && (
        <section className="learning">
          <h2>📈 Learning Curves (This Session)</h2>

          <div className="learning-grid">
            {/* Claude's Epistemic Drift */}
            <div className="learning-card">
              <h3>Claude Epistemic Drift</h3>
              <p className="session-time">Session: {learningState.sessionMinutes} min</p>
              <div className="vector-changes">
                <div className="vector">
                  <span className="label">know</span>
                  <span className="start">{(learningState.claudeVectors.start.know * 100).toFixed(0)}%</span>
                  <span className="arrow">→</span>
                  <span className="current">{(learningState.claudeVectors.current.know * 100).toFixed(0)}%</span>
                  <span className="delta">{learningState.claudeVectors.delta.know}</span>
                </div>
                <div className="vector">
                  <span className="label">do</span>
                  <span className="start">{(learningState.claudeVectors.start.do * 100).toFixed(0)}%</span>
                  <span className="arrow">→</span>
                  <span className="current">{(learningState.claudeVectors.current.do * 100).toFixed(0)}%</span>
                  <span className="delta">{learningState.claudeVectors.delta.do}</span>
                </div>
                <div className="vector">
                  <span className="label">context</span>
                  <span className="start">{(learningState.claudeVectors.start.context * 100).toFixed(0)}%</span>
                  <span className="arrow">→</span>
                  <span className="current">{(learningState.claudeVectors.current.context * 100).toFixed(0)}%</span>
                  <span className="delta">{learningState.claudeVectors.delta.context}</span>
                </div>
                <div className="vector">
                  <span className="label">uncertainty</span>
                  <span className="start">{(learningState.claudeVectors.start.uncertainty * 100).toFixed(0)}%</span>
                  <span className="arrow">→</span>
                  <span className="current">{(learningState.claudeVectors.current.uncertainty * 100).toFixed(0)}%</span>
                  <span className="delta">{learningState.claudeVectors.delta.uncertainty}</span>
                </div>
              </div>
            </div>

            {/* User Capability Growth */}
            <div className="learning-card">
              <h3>User Capability Growth</h3>
              <div className="user-profile">
                <div className="profile-metric">
                  <span className="label">Autonomy Level</span>
                  <div className="progress">
                    <span className="value">{learningState.userProfile.autonomyLevel.start} → {learningState.userProfile.autonomyLevel.current}</span>
                    <span className="desc">{learningState.userProfile.autonomyLevel.description}</span>
                  </div>
                </div>
                <div className="profile-metric">
                  <span className="label">Question Depth</span>
                  <div className="progress">
                    <span className="value">{learningState.userProfile.questionDepth.start} → {learningState.userProfile.questionDepth.current}</span>
                    <span className="desc">{learningState.userProfile.questionDepth.description}</span>
                  </div>
                </div>
                <div className="profile-metric">
                  <span className="label">Error Catch Rate</span>
                  <div className="progress">
                    <span className="value">{(learningState.userProfile.errorCatchRate * 100).toFixed(0)}%</span>
                    <span className="desc">Gaps identified: 2/3 total</span>
                  </div>
                </div>
                <div className="profile-metric">
                  <span className="label">Decision Confidence</span>
                  <div className="progress">
                    <span className="value">{(learningState.userProfile.decisionConfidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Collaboration Multiplier */}
            <div className="learning-card">
              <h3>Collaboration Multiplier</h3>
              <div className="collab-metric">
                <span className="multiplier">{learningState.collaborationMetrics.catchMultiplier}</span>
                <p className="desc">Together vs independent effectiveness</p>
              </div>
              <div className="catch-summary">
                <div className="catches">
                  <h4>Claude caught:</h4>
                  <ul>
                    {learningState.collaborationMetrics.claudeCatches.map((c, i) => (
                      <li key={i}>{c.error} <span className="severity">{c.severity}</span></li>
                    ))}
                  </ul>
                </div>
                <div className="catches">
                  <h4>User caught:</h4>
                  <ul>
                    {learningState.collaborationMetrics.userCatches.map((c, i) => (
                      <li key={i}>{c.gap} <span className="severity">{c.severity}</span></li>
                    ))}
                  </ul>
                </div>
              </div>
              <p className="convergence">Convergence rounds: {learningState.collaborationMetrics.convergenceRounds}</p>
            </div>
          </div>

          {/* Insights */}
          <div className="insights">
            <h3>🧠 Session Insights</h3>
            <ul>
              {learningState.insights.map((insight, i) => (
                <li key={i}>{insight}</li>
              ))}
            </ul>
          </div>
        </section>
      )}

      <footer>
        <p>Mesh Health: <span className="health-ok">✅ Operational</span></p>
        <p>Backend: <a href="/api/health" target="_blank" rel="noreferrer">Health Check</a></p>
      </footer>
    </div>
  );
}

export default App;
