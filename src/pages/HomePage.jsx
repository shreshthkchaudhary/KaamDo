import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { getTasks } from '../api';
import { useAuth } from '../context/AuthContext';
import TaskCard from '../components/TaskCard';

// Fix Leaflet default marker icon issue with bundlers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function MapUpdater({ center }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom());
  }, [center, map]);
  return null;
}

export default function HomePage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [center, setCenter] = useState([12.9716, 77.5946]); // Default: Bangalore
  const [radius, setRadius] = useState(10);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    if (user?.lat && user?.lng) {
      setCenter([user.lat, user.lng]);
    }
  }, [user]);

  useEffect(() => {
    fetchTasks();
  }, [center, radius]);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const res = await getTasks({ lat: center[0], lng: center[1], radius });
      setTasks(res.data.tasks);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredTasks = filter === 'all'
    ? tasks
    : tasks.filter((t) => t.status === filter);

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-bold font-[Syne] text-dark">
            {user?.role === 'worker' ? 'Available Tasks' : 'Task Feed'}
          </h1>
          <p className="text-text-muted mt-1">
            {tasks.length} task{tasks.length !== 1 ? 's' : ''} nearby
          </p>
        </div>

        {/* Radius filter */}
        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-text-muted">Radius:</label>
          <select
            value={radius}
            onChange={(e) => setRadius(Number(e.target.value))}
            className="px-3 py-2 rounded-xl border border-cream-dark bg-white text-sm
                       focus:outline-none focus:ring-2 focus:ring-primary/30"
          >
            <option value={2}>2 km</option>
            <option value={5}>5 km</option>
            <option value={10}>10 km</option>
            <option value={25}>25 km</option>
            <option value={50}>50 km</option>
          </select>
        </div>
      </div>

      {/* Map + List layout */}
      <div className="grid lg:grid-cols-5 gap-6">
        {/* Map */}
        <div className="lg:col-span-3 h-[300px] lg:h-[450px] rounded-2xl overflow-hidden shadow-lg relative z-0">
          <MapContainer center={center} zoom={12} className="h-full w-full">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/">OSM</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <MapUpdater center={center} />
            {filteredTasks.map((t) => (
              <Marker key={t.id} position={[t.lat, t.lng]}>
                <Popup>
                  <div className="text-center">
                    <p className="font-bold text-sm">{t.title}</p>
                    <p className="text-xs text-gray-500">{t.category}</p>
                    <p className="text-sm font-semibold text-green-700 mt-1">₹{t.budget}</p>
                    <button
                      onClick={() => navigate(`/tasks/${t.id}`)}
                      className="mt-2 px-3 py-1 bg-green-700 text-white text-xs rounded-lg
                                 hover:bg-green-600 cursor-pointer"
                    >
                      View Details
                    </button>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        {/* Task List */}
        <div className="lg:col-span-2">
          {/* Status filter tabs */}
          <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
            {['all', 'open', 'assigned', 'completed'].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap
                            transition-all duration-200 cursor-pointer
                  ${filter === f
                    ? 'bg-primary text-white shadow-md'
                    : 'bg-white text-text-muted hover:bg-primary-50 hover:text-primary'
                  }`}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>

          {/* Task cards */}
          <div className="space-y-4 max-h-[400px] lg:max-h-[380px] overflow-y-auto pr-2 stagger">
            {loading ? (
              <div className="text-center py-12 text-text-muted">Loading tasks...</div>
            ) : filteredTasks.length === 0 ? (
              <div className="text-center py-12 glass-card">
                <p className="text-4xl mb-3">📭</p>
                <p className="font-semibold text-dark">No tasks found</p>
                <p className="text-sm text-text-muted mt-1">Try increasing the radius</p>
              </div>
            ) : (
              filteredTasks.map((t) => (
                <TaskCard
                  key={t.id}
                  task={t}
                  onClick={() => navigate(`/tasks/${t.id}`)}
                />
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
