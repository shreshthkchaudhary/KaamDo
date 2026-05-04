import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-md bg-white/80 border-b border-primary-50/50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-9 h-9 rounded-xl bg-primary flex items-center justify-center
                            group-hover:scale-110 transition-transform duration-300">
              <span className="text-white font-bold text-lg font-[Syne]">K</span>
            </div>
            <span className="text-xl font-bold font-[Syne] text-primary">
              Kaam<span className="text-accent">Do</span>
            </span>
          </Link>

          {/* Nav links */}
          <div className="flex items-center gap-3">
            {user ? (
              <>
                <Link
                  to="/home"
                  className="px-3 py-2 text-sm font-medium text-text-muted hover:text-primary
                             transition-colors duration-200"
                >
                  Tasks
                </Link>

                {user.role === 'poster' && (
                  <Link
                    to="/post-task"
                    className="px-4 py-2 text-sm font-semibold text-white bg-primary
                               rounded-xl hover:bg-primary-light transition-all duration-200
                               shadow-md hover:shadow-lg"
                  >
                    + Post Task
                  </Link>
                )}

                {user.role === 'worker' && (
                  <Link
                    to="/worker/dashboard"
                    className="px-3 py-2 text-sm font-medium text-text-muted hover:text-primary
                               transition-colors duration-200"
                  >
                    Dashboard
                  </Link>
                )}

                <Link
                  to={`/profile/${user.id}`}
                  className="px-3 py-2 text-sm font-medium text-text-muted hover:text-primary
                             transition-colors duration-200"
                >
                  Profile
                </Link>

                <button
                  onClick={handleLogout}
                  className="px-3 py-2 text-sm font-medium text-danger hover:bg-danger/10
                             rounded-xl transition-all duration-200 cursor-pointer"
                >
                  Logout
                </button>

                {/* User avatar */}
                <div className="w-9 h-9 rounded-full bg-primary-50 flex items-center justify-center
                                text-sm font-semibold text-primary border-2 border-primary/20">
                  {user.name?.charAt(0)?.toUpperCase()}
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 text-sm font-medium text-primary hover:bg-primary-50
                             rounded-xl transition-all duration-200"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 text-sm font-semibold text-white bg-primary
                             rounded-xl hover:bg-primary-light transition-all duration-200
                             shadow-md hover:shadow-lg"
                >
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
