import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getTasks, getMyBids } from '../api';
import TaskCard from '../components/TaskCard';

export default function WorkerDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [nearbyTasks, setNearbyTasks] = useState([]);
  const [myBids, setMyBids] = useState([]);
  const [tab, setTab] = useState('nearby');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [tasksRes, bidsRes] = await Promise.all([
        getTasks({
          lat: user?.lat || 12.9716,
          lng: user?.lng || 77.5946,
          radius: 15,
        }),
        getMyBids(),
      ]);
      setNearbyTasks(tasksRes.data.tasks.filter(t => t.status === 'open'));
      setMyBids(bidsRes.data.bids);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const activeBids = myBids.filter(b => b.status === 'pending');
  const acceptedBids = myBids.filter(b => b.status === 'accepted');
  const completedBids = myBids.filter(b => b.task_status === 'completed');

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-[Syne] text-dark">Worker Dashboard</h1>
        <p className="text-text-muted mt-1">Find tasks, manage bids, grow your reputation</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 stagger">
        {[
          { label: 'Nearby Tasks', value: nearbyTasks.length, icon: '📍', color: 'bg-primary-50 text-primary' },
          { label: 'Active Bids', value: activeBids.length, icon: '⚡', color: 'bg-accent/10 text-accent-dark' },
          { label: 'Accepted', value: acceptedBids.length, icon: '✅', color: 'bg-success/10 text-success' },
          { label: 'Completed', value: completedBids.length, icon: '🏆', color: 'bg-info/10 text-info' },
        ].map((s) => (
          <div key={s.label} className="glass-card p-5 text-center">
            <p className="text-2xl mb-1">{s.icon}</p>
            <p className="text-3xl font-bold font-[Syne] text-dark">{s.value}</p>
            <p className="text-xs text-text-muted mt-1">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {[
          { key: 'nearby', label: `Nearby Tasks (${nearbyTasks.length})` },
          { key: 'bids', label: `My Bids (${myBids.length})` },
        ].map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all cursor-pointer
              ${tab === t.key
                ? 'bg-primary text-white shadow-md'
                : 'bg-white text-text-muted hover:bg-primary-50'
              }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-12 text-text-muted">Loading...</div>
      ) : tab === 'nearby' ? (
        <div className="grid md:grid-cols-2 gap-4 stagger">
          {nearbyTasks.length === 0 ? (
            <div className="glass-card p-8 text-center col-span-2">
              <p className="text-4xl mb-3">🔍</p>
              <p className="font-semibold text-dark">No open tasks nearby</p>
              <p className="text-sm text-text-muted">Check back later!</p>
            </div>
          ) : (
            nearbyTasks.map((t) => (
              <TaskCard key={t.id} task={t} onClick={() => navigate(`/tasks/${t.id}`)} />
            ))
          )}
        </div>
      ) : (
        <div className="space-y-4 stagger">
          {myBids.length === 0 ? (
            <div className="glass-card p-8 text-center">
              <p className="text-4xl mb-3">📋</p>
              <p className="font-semibold text-dark">No bids placed yet</p>
              <p className="text-sm text-text-muted">Browse nearby tasks and start bidding!</p>
            </div>
          ) : (
            myBids.map((bid) => (
              <div
                key={bid.id}
                onClick={() => navigate(`/tasks/${bid.task_id}`)}
                className="glass-card p-5 cursor-pointer hover:border-primary/30"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-dark">{bid.task_title}</p>
                    <p className="text-sm text-text-muted mt-1">
                      Your bid: <span className="font-bold text-primary">₹{bid.amount}</span>
                      {' · '}Task budget: ₹{bid.task_budget}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold
                    ${bid.status === 'pending' ? 'bg-accent/10 text-accent-dark'
                      : bid.status === 'accepted' ? 'bg-success/10 text-success'
                        : 'bg-danger/10 text-danger'
                    }`}>
                    {bid.status?.toUpperCase()}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
