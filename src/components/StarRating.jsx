export default function StarRating({ rating = 0, size = 'md', showValue = true }) {
  const stars = [];
  const fullStars = Math.floor(rating);
  const hasHalf = rating % 1 >= 0.3;
  const sizeClass = size === 'sm' ? 'text-sm' : size === 'lg' ? 'text-2xl' : 'text-lg';

  for (let i = 0; i < 5; i++) {
    if (i < fullStars) {
      stars.push(<span key={i} className="text-accent">★</span>);
    } else if (i === fullStars && hasHalf) {
      stars.push(<span key={i} className="text-accent/50">★</span>);
    } else {
      stars.push(<span key={i} className="text-gray-300">★</span>);
    }
  }

  return (
    <span className={`inline-flex items-center gap-1 ${sizeClass}`}>
      {stars}
      {showValue && (
        <span className="text-text-muted text-sm ml-1">
          {rating > 0 ? rating.toFixed(1) : 'N/A'}
        </span>
      )}
    </span>
  );
}
