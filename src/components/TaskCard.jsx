export default function TaskCard({ task, onClick }) {
  const statusColors = {
    open: 'bg-success/10 text-success',
    assigned: 'bg-info/10 text-info',
    completed: 'bg-primary-50 text-primary',
    cancelled: 'bg-danger/10 text-danger',
  };

  return (
    <div
      onClick={onClick}
      className="glass-card p-5 cursor-pointer hover:border-primary/30 group"
    >
      <div className="flex items-start justify-between mb-3">
        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${
            statusColors[task.status] || 'bg-gray-100 text-gray-600'
          }`}
        >
          {task.status?.toUpperCase()}
        </span>
        {task.category && (
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-accent/10 text-accent-dark">
            {task.category}
          </span>
        )}
      </div>

      <h3 className="text-lg font-semibold font-[Syne] text-dark mb-2
                      group-hover:text-primary transition-colors duration-200">
        {task.title}
      </h3>

      <p className="text-sm text-text-muted line-clamp-2 mb-4">
        {task.description}
      </p>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl font-bold text-primary font-[Syne]">
            ₹{task.budget}
          </span>
          {task.suggested_price_min && task.suggested_price_max && (
            <span className="text-xs text-text-muted">
              (AI: ₹{task.suggested_price_min}–₹{task.suggested_price_max})
            </span>
          )}
        </div>
        {task.distance_km !== undefined && (
          <span className="text-xs text-text-muted bg-cream-dark px-2 py-1 rounded-lg">
            📍 {task.distance_km} km
          </span>
        )}
      </div>
    </div>
  );
}
