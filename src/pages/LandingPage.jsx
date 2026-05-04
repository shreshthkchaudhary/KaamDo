import { Link } from 'react-router-dom';

const FEATURES = [
  { icon: '🎯', title: 'Post Any Task', desc: 'Fix a fan, find a tutor, move furniture — post it and let workers come to you.' },
  { icon: '🤖', title: 'AI-Powered Matching', desc: 'Smart classification, fair pricing, and worker matching powered by real ML models.' },
  { icon: '💰', title: 'Escrow Protection', desc: 'Payment is locked until the task is done. Safe for both sides.' },
  { icon: '📍', title: 'Hyperlocal', desc: 'Find help within walking distance. Map-based discovery for nearby tasks.' },
  { icon: '⚡', title: 'Real-Time Bids', desc: 'Workers bid live. See offers appear instantly with match scores.' },
  { icon: '⭐', title: 'Verified Ratings', desc: 'Both sides rate each other. Build trust with every completed task.' },
];

const STEPS = [
  { num: '01', title: 'Post Your Task', desc: 'Describe what you need. Our AI auto-classifies and suggests a fair price.' },
  { num: '02', title: 'Get Bids', desc: 'Nearby workers see your task and place competitive bids in real time.' },
  { num: '03', title: 'Choose & Pay', desc: 'Pick the best worker. Payment is held in escrow until task completion.' },
];

const CATEGORIES = [
  { emoji: '🔧', name: 'Home Repair' },
  { emoji: '📚', name: 'Education' },
  { emoji: '🚚', name: 'Delivery' },
  { emoji: '💪', name: 'Labour & Moving' },
  { emoji: '🧹', name: 'Cleaning' },
  { emoji: '💻', name: 'Tech Help' },
  { emoji: '📦', name: 'General' },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary via-primary-light to-primary-dark
                          pt-20 pb-28 px-4">
        {/* Decorative circles */}
        <div className="absolute top-10 right-10 w-72 h-72 bg-accent/10 rounded-full blur-3xl" />
        <div className="absolute bottom-10 left-10 w-96 h-96 bg-white/5 rounded-full blur-3xl" />

        <div className="max-w-7xl mx-auto text-center relative z-10">
          <div className="animate-fadeInUp">
            <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 text-white/90
                             text-sm font-medium mb-6 backdrop-blur-sm border border-white/20">
              🚀 India's Hyperlocal Task Marketplace
            </span>

            <h1 className="text-5xl md:text-7xl font-bold text-white font-[Syne] mb-6
                           leading-tight tracking-tight">
              Get Anything Done,
              <br />
              <span className="text-accent">Right Next Door</span>
            </h1>

            <p className="text-lg md:text-xl text-white/80 max-w-2xl mx-auto mb-10 leading-relaxed">
              Post any task. Workers nearby bid with their price.
              AI matches the best worker for your job. Simple.
            </p>

            <div className="flex items-center justify-center gap-4 flex-wrap">
              <Link
                to="/register"
                className="px-8 py-4 bg-accent text-dark font-bold text-lg rounded-2xl
                           hover:bg-accent-light transition-all duration-300 shadow-xl
                           hover:shadow-2xl hover:scale-105"
              >
                Start Posting Tasks →
              </Link>
              <Link
                to="/register"
                className="px-8 py-4 bg-white/10 text-white font-semibold text-lg rounded-2xl
                           border border-white/30 hover:bg-white/20 transition-all duration-300
                           backdrop-blur-sm"
              >
                Join as Worker
              </Link>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-3 gap-8 max-w-lg mx-auto animate-fadeInUp"
            style={{ animationDelay: '0.3s' }}>
            {[
              { num: '7', label: 'Categories' },
              { num: 'AI', label: 'Powered' },
              { num: '₹0', label: 'To Start' },
            ].map((s) => (
              <div key={s.label} className="text-center">
                <p className="text-3xl font-bold text-accent font-[Syne]">{s.num}</p>
                <p className="text-sm text-white/60">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories ribbon */}
      <section className="py-6 bg-white/50 border-y border-cream-dark">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-center gap-6 flex-wrap">
          {CATEGORIES.map((c) => (
            <span key={c.name} className="flex items-center gap-2 px-4 py-2 rounded-full
                                          bg-cream text-sm font-medium text-dark hover:bg-primary-50
                                          hover:text-primary transition-all duration-200 cursor-default">
              <span className="text-lg">{c.emoji}</span>
              {c.name}
            </span>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4 max-w-7xl mx-auto">
        <div className="text-center mb-14">
          <h2 className="text-4xl font-bold font-[Syne] text-dark mb-3">
            How It Works
          </h2>
          <p className="text-text-muted text-lg">Three simple steps to get stuff done</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 stagger">
          {STEPS.map((step) => (
            <div key={step.num} className="glass-card p-8 text-center relative overflow-hidden group">
              <span className="text-7xl font-black font-[Syne] text-primary/5 absolute -top-4 -right-2
                               group-hover:text-primary/10 transition-colors duration-500">
                {step.num}
              </span>
              <div className="relative z-10">
                <div className="w-14 h-14 mx-auto rounded-2xl bg-primary-50 flex items-center
                                justify-center text-primary font-bold text-xl font-[Syne] mb-5">
                  {step.num}
                </div>
                <h3 className="text-xl font-bold font-[Syne] mb-3">{step.title}</h3>
                <p className="text-text-muted leading-relaxed">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-4 bg-white/40">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-4xl font-bold font-[Syne] text-dark mb-3">
              Why KaamDo?
            </h2>
            <p className="text-text-muted text-lg">Built with AI, designed for trust</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 stagger">
            {FEATURES.map((f) => (
              <div key={f.title} className="glass-card p-6 group">
                <span className="text-3xl mb-4 block">{f.icon}</span>
                <h3 className="text-lg font-bold font-[Syne] mb-2 group-hover:text-primary
                               transition-colors duration-200">
                  {f.title}
                </h3>
                <p className="text-sm text-text-muted leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4">
        <div className="max-w-3xl mx-auto text-center glass-card p-12 bg-gradient-to-br
                        from-primary to-primary-dark border-none">
          <h2 className="text-3xl md:text-4xl font-bold font-[Syne] text-white mb-4">
            Ready to Get Things Done?
          </h2>
          <p className="text-white/80 text-lg mb-8">
            Join KaamDo and connect with skilled workers in your neighborhood.
          </p>
          <Link
            to="/register"
            className="inline-block px-8 py-4 bg-accent text-dark font-bold text-lg
                       rounded-2xl hover:bg-accent-light transition-all duration-300
                       shadow-xl hover:shadow-2xl"
          >
            Get Started Free →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-cream-dark">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <span className="text-sm text-text-muted">
            © 2026 KaamDo. Built with ❤️ and AI.
          </span>
          <span className="text-sm font-semibold font-[Syne] text-primary">
            Kaam<span className="text-accent">Do</span>
          </span>
        </div>
      </footer>
    </div>
  );
}
