import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getUserRatings } from '../api';
import { useAuth } from '../context/AuthContext';
import StarRating from '../components/StarRating';

export default function ProfilePage() {
  const { id } = useParams();
  const { user: currentUser } = useAuth();
  const [ratings, setRatings] = useState([]);
  const [avgRating, setAvgRating] = useState(0);
  const [loading, setLoading] = useState(true);

  // For now, show current user's info (we'd need a get user endpoint for other profiles)
  const isOwnProfile = currentUser && String(currentUser.id) === id;
  const profileUser = isOwnProfile ? currentUser : null;

  useEffect(() => {
    fetchRatings();
  }, [id]);

  const fetchRatings = async () => {
    try {
      const res = await getUserRatings(id);
      setRatings(res.data.ratings);
      setAvgRating(res.data.avg_rating);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-text-muted">Loading profile...</div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 animate-fadeInUp">
      {/* Profile header */}
      <div className="glass-card p-8 mb-6 text-center">
        <div className="w-20 h-20 mx-auto rounded-full bg-primary flex items-center justify-center
                        text-3xl font-bold text-white font-[Syne] mb-4 shadow-lg">
          {profileUser?.name?.charAt(0)?.toUpperCase() || '?'}
        </div>
        <h1 className="text-2xl font-bold font-[Syne] text-dark">
          {profileUser?.name || `User #${id}`}
        </h1>
        <p className="text-text-muted mt-1">{profileUser?.email}</p>

        <div className="flex items-center justify-center gap-6 mt-4">
          <div className="text-center">
            <p className="text-sm text-text-muted">Role</p>
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-primary-50 text-primary mt-1 inline-block">
              {profileUser?.role?.toUpperCase() || 'USER'}
            </span>
          </div>
          <div className="text-center">
            <p className="text-sm text-text-muted">Rating</p>
            <StarRating rating={avgRating} size="lg" />
          </div>
          <div className="text-center">
            <p className="text-sm text-text-muted">Tasks</p>
            <p className="text-xl font-bold text-dark">{profileUser?.total_tasks || 0}</p>
          </div>
        </div>

        {/* Skills */}
        {profileUser?.skills && (
          <div className="mt-4">
            <p className="text-sm text-text-muted mb-2">Skills</p>
            <div className="flex flex-wrap justify-center gap-2">
              {profileUser.skills.split(',').map((s) => (
                <span key={s} className="px-3 py-1 rounded-full text-xs font-medium
                                         bg-accent/10 text-accent-dark">
                  {s.trim()}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Ratings */}
      <h2 className="text-xl font-bold font-[Syne] text-dark mb-4">
        Reviews ({ratings.length})
      </h2>
      <div className="space-y-4 stagger">
        {ratings.length === 0 ? (
          <div className="glass-card p-8 text-center">
            <p className="text-3xl mb-2">📝</p>
            <p className="text-text-muted">No reviews yet</p>
          </div>
        ) : (
          ratings.map((r) => (
            <div key={r.id} className="glass-card p-5">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-primary-50 flex items-center
                                  justify-center text-xs font-bold text-primary">
                    {r.rater_name?.charAt(0)?.toUpperCase()}
                  </div>
                  <span className="font-semibold text-sm text-dark">{r.rater_name}</span>
                </div>
                <StarRating rating={r.score} size="sm" showValue={false} />
              </div>
              {r.comment && (
                <p className="text-sm text-text-muted italic">"{r.comment}"</p>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
