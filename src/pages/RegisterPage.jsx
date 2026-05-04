import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { registerUser } from '../api';

export default function RegisterPage() {
  const [form, setForm] = useState({
    name: '', email: '', password: '', role: 'poster', skills: '', lat: '', lng: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const detectLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setForm((f) => ({
          ...f, lat: pos.coords.latitude.toFixed(6), lng: pos.coords.longitude.toFixed(6)
        })),
        () => setError('Location access denied. You can enter coordinates manually.')
      );
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const payload = {
        ...form,
        lat: form.lat ? parseFloat(form.lat) : null,
        lng: form.lng ? parseFloat(form.lng) : null,
        skills: form.role === 'worker' ? form.skills : null,
      };
      const res = await registerUser(payload);
      login(res.data.token, res.data.user);
      navigate('/home');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const SKILL_OPTIONS = [
    'Home Repair', 'Education', 'Delivery', 'Labour & Moving',
    'Cleaning', 'Tech Help', 'General'
  ];

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-lg animate-fadeInUp">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold font-[Syne] text-dark mb-2">Join KaamDo</h1>
          <p className="text-text-muted">Create your account and start getting things done</p>
        </div>

        <form onSubmit={handleSubmit} className="glass-card p-8 space-y-5">
          {error && (
            <div className="p-3 rounded-xl bg-danger/10 text-danger text-sm font-medium">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-semibold text-dark mb-1.5">Full Name</label>
            <input
              id="reg-name" type="text" required value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                         focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                         transition-all duration-200"
              placeholder="Your name"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-dark mb-1.5">Email</label>
            <input
              id="reg-email" type="email" required value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                         focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                         transition-all duration-200"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-dark mb-1.5">Password</label>
            <input
              id="reg-password" type="password" required minLength={6} value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                         focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                         transition-all duration-200"
              placeholder="Min 6 characters"
            />
          </div>

          {/* Role selector */}
          <div>
            <label className="block text-sm font-semibold text-dark mb-2">I want to</label>
            <div className="grid grid-cols-2 gap-3">
              {[
                { val: 'poster', label: '📋 Post Tasks', desc: 'Get things done' },
                { val: 'worker', label: '🔨 Do Tasks', desc: 'Earn money' },
              ].map((r) => (
                <button
                  key={r.val}
                  type="button"
                  onClick={() => setForm({ ...form, role: r.val })}
                  className={`p-4 rounded-xl border-2 text-left transition-all duration-200 cursor-pointer
                    ${form.role === r.val
                      ? 'border-primary bg-primary-50'
                      : 'border-cream-dark bg-cream/30 hover:border-primary/30'
                    }`}
                >
                  <p className="font-semibold text-sm">{r.label}</p>
                  <p className="text-xs text-text-muted mt-0.5">{r.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Skills (workers only) */}
          {form.role === 'worker' && (
            <div>
              <label className="block text-sm font-semibold text-dark mb-2">Your Skills</label>
              <div className="flex flex-wrap gap-2">
                {SKILL_OPTIONS.map((skill) => {
                  const selected = form.skills.toLowerCase().includes(skill.toLowerCase());
                  return (
                    <button
                      key={skill}
                      type="button"
                      onClick={() => {
                        const current = form.skills.split(',').map(s => s.trim()).filter(Boolean);
                        const updated = selected
                          ? current.filter(s => s.toLowerCase() !== skill.toLowerCase())
                          : [...current, skill];
                        setForm({ ...form, skills: updated.join(', ') });
                      }}
                      className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all
                                  duration-200 cursor-pointer
                        ${selected
                          ? 'bg-primary text-white'
                          : 'bg-cream-dark text-text-muted hover:bg-primary-50 hover:text-primary'
                        }`}
                    >
                      {skill}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Location */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-sm font-semibold text-dark">Location</label>
              <button
                type="button"
                onClick={detectLocation}
                className="text-xs text-primary font-medium hover:underline cursor-pointer"
              >
                📍 Detect my location
              </button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <input
                type="number" step="any" value={form.lat}
                onChange={(e) => setForm({ ...form, lat: e.target.value })}
                className="px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                           focus:outline-none focus:ring-2 focus:ring-primary/30
                           transition-all duration-200"
                placeholder="Latitude"
              />
              <input
                type="number" step="any" value={form.lng}
                onChange={(e) => setForm({ ...form, lng: e.target.value })}
                className="px-4 py-3 rounded-xl border border-cream-dark bg-cream/50
                           focus:outline-none focus:ring-2 focus:ring-primary/30
                           transition-all duration-200"
                placeholder="Longitude"
              />
            </div>
          </div>

          <button
            type="submit" disabled={loading}
            className="w-full py-3.5 bg-primary text-white font-bold rounded-xl
                       hover:bg-primary-light transition-all duration-200 shadow-lg
                       hover:shadow-xl disabled:opacity-50 cursor-pointer"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>

          <p className="text-center text-sm text-text-muted">
            Already have an account?{' '}
            <Link to="/login" className="text-primary font-semibold hover:underline">
              Log in
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
