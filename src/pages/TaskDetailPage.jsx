import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { io } from 'socket.io-client';
import { getTask, getTaskBids, placeBid, acceptBid, updateTaskStatus, submitRating } from '../api';
import { useAuth } from '../context/AuthContext';
import BidCard from '../components/BidCard';
import StarRating from '../components/StarRating';

export default function TaskDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [task, setTask] = useState(null);
  const [bids, setBids] = useState([]);
  const [loading, setLoading] = useState(true);
  const [bidForm, setBidForm] = useState({ amount: '', message: '' });
  const [bidding, setBidding] = useState(false);
  const [ratingForm, setRatingForm] = useState({ score: 5, comment: '' });
  const [showRating, setShowRating] = useState(false);

  useEffect(() => {
    fetchData();

    // Connect to SocketIO for real-time bids
    const SOCKET_URL = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('/api', '') : '/';
    const socket = io(SOCKET_URL, { transports: ['websocket', 'polling'] });
    socket.emit('join_task', { task_id: parseInt(id) });

    socket.on('new_bid', (bid) => {
      setBids((prev) => {
        if (prev.find(b => b.id === bid.id)) return prev;
        return [...prev, bid];
      });
    });

    socket.on('bid_accepted', (data) => {
      setBids((prev) =>
        prev.map((b) =>
          b.id === data.bid_id ? { ...b, status: 'accepted' }
            : b.task_id === data.task_id && b.status === 'pending'
              ? { ...b, status: 'rejected' } : b
        )
      );
      setTask((prev) => prev ? { ...prev, status: 'assigned' } : prev);
    });

    return () => {
      socket.emit('leave_task', { task_id: parseInt(id) });
      socket.disconnect();
    };
  }, [id]);

  const fetchData = async () => {
    try {
      const [taskRes, bidsRes] = await Promise.all([
        getTask(id), getTaskBids(id)
      ]);
      setTask(taskRes.data.task);
      setBids(bidsRes.data.bids);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePlaceBid = async (e) => {
    e.preventDefault();
    setBidding(true);
    try {
      await placeBid({
        task_id: parseInt(id),
        amount: parseFloat(bidForm.amount),
        message: bidForm.message,
      });
      setBidForm({ amount: '', message: '' });
      // Bid will appear via SocketIO
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to place bid');
    } finally {
      setBidding(false);
    }
  };

  const handleAcceptBid = async (bidId) => {
    try {
      await acceptBid(bidId);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to accept bid');
    }
  };

  const handleComplete = async () => {
    try {
      await updateTaskStatus(id, 'completed');
      setTask((prev) => ({ ...prev, status: 'completed' }));
      setShowRating(true);
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to complete task');
    }
  };

  const handleRate = async (e) => {
    e.preventDefault();
    try {
      const acceptedBid = bids.find(b => b.status === 'accepted');
      const rateeId = user.id === task.poster_id
        ? acceptedBid?.worker_id
        : task.poster_id;

      await submitRating({
        ratee_id: rateeId,
        task_id: parseInt(id),
        score: ratingForm.score,
        comment: ratingForm.comment,
      });
      setShowRating(false);
      alert('Rating submitted!');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to submit rating');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-text-muted text-lg">Loading task...</div>
      </div>
    );
  }
  if (!task) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-danger text-lg">Task not found</div>
      </div>
    );
  }

  const isOwnTask = user?.id === task.poster_id;
  const acceptedBid = bids.find(b => b.status === 'accepted');

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 animate-fadeInUp">
      {/* Task Header */}
      <div className="glass-card p-8 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              {task.category && (
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-accent/10 text-accent-dark">
                  {task.category}
                </span>
              )}
              <span className={`px-3 py-1 rounded-full text-xs font-semibold
                ${task.status === 'open' ? 'bg-success/10 text-success'
                  : task.status === 'assigned' ? 'bg-info/10 text-info'
                  : task.status === 'completed' ? 'bg-primary-50 text-primary'
                  : 'bg-danger/10 text-danger'
                }`}>
                {task.status?.toUpperCase()}
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold font-[Syne] text-dark">{task.title}</h1>
          </div>
          <div className="text-right">
            <p className="text-3xl font-bold text-primary font-[Syne]">₹{task.budget}</p>
            {task.suggested_price_min && (
              <p className="text-xs text-text-muted mt-1">
                AI: ₹{task.suggested_price_min}–₹{task.suggested_price_max}
              </p>
            )}
          </div>
        </div>

        <p className="text-text-muted leading-relaxed mb-4">{task.description}</p>

        <div className="flex items-center gap-4 text-sm text-text-muted">
          <span>📍 {task.lat?.toFixed(4)}, {task.lng?.toFixed(4)}</span>
          <span>📏 {task.radius_km} km radius</span>
          <span>👤 Posted by {task.poster_name}</span>
        </div>

        {task.photo_path && (
          <div className="mt-4">
            <img src={`/uploads/${task.photo_path}`} alt="Task"
                 className="max-h-60 rounded-xl object-cover" />
          </div>
        )}

        {/* Escrow status */}
        {task.status === 'assigned' && acceptedBid && (
          <div className="mt-4 p-4 rounded-xl bg-accent/10 border border-accent/30">
            <p className="font-semibold text-accent-dark">
              🔒 ₹{acceptedBid.amount} locked in escrow
            </p>
            {isOwnTask && (
              <button
                onClick={handleComplete}
                className="mt-3 px-6 py-2.5 bg-success text-white font-semibold rounded-xl
                           hover:bg-green-600 transition-all cursor-pointer"
              >
                ✅ Mark Task Complete — Release Payment
              </button>
            )}
          </div>
        )}

        {task.status === 'completed' && acceptedBid && (
          <div className="mt-4 p-4 rounded-xl bg-success/10 border border-success/30">
            <p className="font-semibold text-success">
              ✅ ₹{acceptedBid.amount} released to worker
            </p>
          </div>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Bids section */}
        <div>
          <h2 className="text-xl font-bold font-[Syne] text-dark mb-4">
            Bids ({bids.length})
          </h2>
          <div className="space-y-4">
            {bids.length === 0 ? (
              <div className="glass-card p-8 text-center">
                <p className="text-3xl mb-2">🕐</p>
                <p className="text-text-muted">No bids yet. Workers will bid soon!</p>
              </div>
            ) : (
              bids.map((bid) => (
                <BidCard
                  key={bid.id}
                  bid={bid}
                  isOwnTask={isOwnTask}
                  onAccept={handleAcceptBid}
                />
              ))
            )}
          </div>
        </div>

        {/* Place bid / Rating section */}
        <div>
          {/* Bid form for workers */}
          {user?.role === 'worker' && task.status === 'open' && !isOwnTask && (
            <div className="glass-card p-6 mb-6">
              <h2 className="text-xl font-bold font-[Syne] text-dark mb-4">Place Your Bid</h2>
              <form onSubmit={handlePlaceBid} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-dark mb-1.5">
                    Your Price (₹)
                  </label>
                  <input
                    type="number" required min="1" value={bidForm.amount}
                    onChange={(e) => setBidForm({ ...bidForm, amount: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                               focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
                    placeholder="Enter your price"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-dark mb-1.5">
                    Message <span className="text-text-muted font-normal">(optional)</span>
                  </label>
                  <textarea
                    rows={3} value={bidForm.message}
                    onChange={(e) => setBidForm({ ...bidForm, message: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                               focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all
                               resize-none"
                    placeholder="Why should they pick you?"
                  />
                </div>
                <button
                  type="submit" disabled={bidding}
                  className="w-full py-3 bg-primary text-white font-bold rounded-xl
                             hover:bg-primary-light transition-all cursor-pointer
                             disabled:opacity-50 shadow-md"
                >
                  {bidding ? 'Placing bid...' : 'Submit Bid'}
                </button>
              </form>
            </div>
          )}

          {/* Rating form */}
          {(showRating || (task.status === 'completed' && user)) && (
            <div className="glass-card p-6">
              <h2 className="text-xl font-bold font-[Syne] text-dark mb-4">Rate & Review</h2>
              <form onSubmit={handleRate} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-dark mb-2">Rating</label>
                  <div className="flex gap-2">
                    {[1, 2, 3, 4, 5].map((s) => (
                      <button
                        key={s} type="button"
                        onClick={() => setRatingForm({ ...ratingForm, score: s })}
                        className={`w-10 h-10 rounded-xl text-lg cursor-pointer transition-all
                          ${ratingForm.score >= s
                            ? 'bg-accent text-white scale-110'
                            : 'bg-cream-dark text-text-muted hover:bg-accent/20'
                          }`}
                      >
                        ★
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-dark mb-1.5">Comment</label>
                  <textarea
                    rows={2} value={ratingForm.comment}
                    onChange={(e) => setRatingForm({ ...ratingForm, comment: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                               focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all
                               resize-none"
                    placeholder="How was the experience?"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full py-3 bg-accent text-dark font-bold rounded-xl
                             hover:bg-accent-light transition-all cursor-pointer shadow-md"
                >
                  Submit Rating
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
