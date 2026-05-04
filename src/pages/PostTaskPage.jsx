import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { createTask, classifyTask, estimatePrice } from '../api';

export default function PostTaskPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: '', description: '', budget: '', lat: '', lng: '', radius_km: '5',
  });
  const [aiResult, setAiResult] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [photo, setPhoto] = useState(null);

  // Auto-fill location from user profile
  useEffect(() => {
    if (user?.lat && user?.lng) {
      setForm((f) => ({ ...f, lat: String(user.lat), lng: String(user.lng) }));
    }
  }, [user]);

  // Debounced AI classification
  const classifyDescription = useCallback(
    (() => {
      let timer;
      return (desc) => {
        clearTimeout(timer);
        if (desc.length < 10) { setAiResult(null); return; }
        timer = setTimeout(async () => {
          setAiLoading(true);
          try {
            const classRes = await classifyTask(desc);
            const cat = classRes.data.category;
            const confidence = classRes.data.confidence;

            const priceRes = await estimatePrice(cat, parseFloat(form.radius_km) || 5);
            setAiResult({
              category: cat,
              confidence,
              min_price: priceRes.data.min_price,
              max_price: priceRes.data.max_price,
            });
          } catch {
            // Silently fail — AI isn't critical
          } finally {
            setAiLoading(false);
          }
        }, 1000);
      };
    })(),
    [form.radius_km]
  );

  const handleDescriptionChange = (e) => {
    const desc = e.target.value;
    setForm({ ...form, description: desc });
    classifyDescription(desc);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      const formData = new FormData();
      formData.append('title', form.title);
      formData.append('description', form.description);
      formData.append('budget', form.budget);
      formData.append('lat', form.lat);
      formData.append('lng', form.lng);
      formData.append('radius_km', form.radius_km);

      if (aiResult) {
        formData.append('category', aiResult.category);
        formData.append('suggested_price_min', aiResult.min_price);
        formData.append('suggested_price_max', aiResult.max_price);
      }
      if (photo) {
        formData.append('photo', photo);
      }

      const res = await createTask(formData);
      navigate(`/tasks/${res.data.task.id}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create task');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-10 animate-fadeInUp">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold font-[Syne] text-dark mb-2">Post a New Task</h1>
        <p className="text-text-muted">Describe what you need — our AI will help classify and price it</p>
      </div>

      <form onSubmit={handleSubmit} className="glass-card p-8 space-y-6">
        {error && (
          <div className="p-3 rounded-xl bg-danger/10 text-danger text-sm font-medium">{error}</div>
        )}

        {/* Title */}
        <div>
          <label className="block text-sm font-semibold text-dark mb-1.5">Task Title</label>
          <input
            id="task-title" type="text" required value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                       focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                       transition-all duration-200"
            placeholder="e.g., Fix my ceiling fan"
          />
        </div>

        {/* Description + AI classification */}
        <div>
          <label className="block text-sm font-semibold text-dark mb-1.5">Description</label>
          <textarea
            id="task-description" required rows={4} value={form.description}
            onChange={handleDescriptionChange}
            className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                       focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                       transition-all duration-200 resize-none"
            placeholder="Describe your task in detail..."
          />

          {/* AI classification result */}
          {aiLoading && (
            <div className="mt-3 px-4 py-3 rounded-xl bg-primary-50 border border-primary/20
                            text-sm text-primary animate-pulse">
              🤖 AI is analyzing your task...
            </div>
          )}

          {aiResult && !aiLoading && (
            <div className="mt-3 px-4 py-3 rounded-xl bg-primary-50 border border-primary/20
                            text-sm animate-fadeInUp">
              <div className="flex items-center gap-3 flex-wrap">
                <span className="font-semibold text-primary">
                  Detected: {aiResult.category}
                </span>
                <span className="text-text-muted">·</span>
                <span className="text-accent-dark font-medium">
                  Suggested Price: ₹{aiResult.min_price} – ₹{aiResult.max_price}
                </span>
                <span className="text-text-muted">·</span>
                <span className="text-text-muted">
                  Confidence: {aiResult.confidence}%
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Budget */}
        <div>
          <label className="block text-sm font-semibold text-dark mb-1.5">
            Your Budget (₹)
            {aiResult && (
              <span className="text-xs text-text-muted font-normal ml-2">
                AI suggests ₹{aiResult.min_price}–₹{aiResult.max_price}
              </span>
            )}
          </label>
          <input
            id="task-budget" type="number" required min="50" value={form.budget}
            onChange={(e) => setForm({ ...form, budget: e.target.value })}
            className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                       focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                       transition-all duration-200"
            placeholder="Enter your budget"
          />
        </div>

        {/* Location & Radius */}
        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="block text-sm font-semibold text-dark mb-1.5">Latitude</label>
            <input
              type="number" step="any" required value={form.lat}
              onChange={(e) => setForm({ ...form, lat: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                         focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
              placeholder="Lat"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-dark mb-1.5">Longitude</label>
            <input
              type="number" step="any" required value={form.lng}
              onChange={(e) => setForm({ ...form, lng: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                         focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
              placeholder="Lng"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-dark mb-1.5">Radius (km)</label>
            <select
              value={form.radius_km}
              onChange={(e) => setForm({ ...form, radius_km: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                         focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
            >
              <option value="2">2 km</option>
              <option value="5">5 km</option>
              <option value="10">10 km</option>
              <option value="15">15 km</option>
            </select>
          </div>
        </div>

        {/* Photo upload */}
        <div>
          <label className="block text-sm font-semibold text-dark mb-1.5">
            Photo <span className="text-text-muted font-normal">(optional)</span>
          </label>
          <input
            type="file" accept="image/*"
            onChange={(e) => setPhoto(e.target.files[0])}
            className="w-full text-sm text-text-muted file:mr-4 file:py-2 file:px-4
                       file:rounded-xl file:border-0 file:bg-primary-50 file:text-primary
                       file:font-semibold file:cursor-pointer hover:file:bg-primary/10"
          />
        </div>

        <button
          type="submit" disabled={submitting}
          className="w-full py-3.5 bg-primary text-white font-bold rounded-xl
                     hover:bg-primary-light transition-all duration-200 shadow-lg
                     hover:shadow-xl disabled:opacity-50 cursor-pointer text-lg"
        >
          {submitting ? 'Posting...' : 'Post Task →'}
        </button>
      </form>
    </div>
  );
}
