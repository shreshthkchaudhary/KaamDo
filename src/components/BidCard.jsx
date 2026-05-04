import StarRating from './StarRating';

export default function BidCard({ bid, isOwnTask, onAccept }) {
  const statusColors = {
    pending: 'bg-accent/10 text-accent-dark',
    accepted: 'bg-success/10 text-success',
    rejected: 'bg-danger/10 text-danger',
  };

  return (
    <div className="glass-card p-5 animate-fadeInUp">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary-50 flex items-center justify-center
                          text-sm font-bold text-primary">
            {bid.worker_name?.charAt(0)?.toUpperCase()}
          </div>
          <div>
            <p className="font-semibold text-dark">{bid.worker_name}</p>
            <StarRating rating={bid.worker_rating || 0} size="sm" />
          </div>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${
            statusColors[bid.status] || 'bg-gray-100 text-gray-600'
          }`}
        >
          {bid.status?.toUpperCase()}
        </span>
      </div>

      <div className="flex items-center gap-2 mb-2">
        <span className="text-2xl font-bold text-primary font-[Syne]">₹{bid.amount}</span>
        {bid.match_score && (
          <span className="px-2 py-0.5 rounded-lg text-xs font-medium bg-primary-50 text-primary">
            Match: {bid.match_score}%
          </span>
        )}
      </div>

      {bid.message && (
        <p className="text-sm text-text-muted mb-3 italic">"{bid.message}"</p>
      )}

      {isOwnTask && bid.status === 'pending' && (
        <button
          onClick={() => onAccept(bid.id)}
          className="w-full py-2.5 bg-primary text-white font-semibold rounded-xl
                     hover:bg-primary-light transition-all duration-200 shadow-md
                     hover:shadow-lg cursor-pointer"
        >
          Accept Bid — Lock ₹{bid.amount} in Escrow
        </button>
      )}

      {bid.status === 'accepted' && (
        <div className="w-full py-2.5 bg-success/10 text-success font-semibold
                        rounded-xl text-center">
          ✅ Accepted — ₹{bid.amount} locked in escrow
        </div>
      )}
    </div>
  );
}
