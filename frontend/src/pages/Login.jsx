import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import api from '../api';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  // LeadBot State
  const [chatVisible, setChatVisible] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! I'm LeadBot. Welcome to TaskVision. Need help logging in or want to explore our demo accounts? 🚀", sender: 'ai' }
  ]);
  const [aiInput, setAiInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await api.post('auth/login/', {
        username: email,
        password: password
      });

      const data = response.data;
      const userData = {
        token: data.token,
        user_id: data.user_id,
        role: data.role,
        name: data.name || email.split('@')[0],
        email: data.email
      };

      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(userData));

      Swal.fire({
        title: 'Login Successful!',
        html: `
            <p>Welcome back${data.name ? ', ' + data.name : ''}!</p>
            <p>Redirecting to dashboard...</p>
        `,
        icon: 'success',
        timer: 1500,
        showConfirmButton: false,
        timerProgressBar: true
      }).then(() => {
        navigate('/');
      });
    } catch (err) {
      console.error('Login error:', err);
      Swal.fire('Login Failed', err.response?.data?.non_field_errors?.[0] || 'Invalid email or password', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fillDemoAccount = (role) => {
    let demoEmail, demoPassword;
    switch (role) {
      case 'po':
        demoEmail = 'po@taskvision.com';
        demoPassword = 'password123';
        break;
      case 'pm':
        demoEmail = 'pm@taskvision.com';
        demoPassword = 'password123';
        break;
      case 'tm':
        demoEmail = 'tm1@taskvision.com';
        demoPassword = 'password123';
        break;
    }
    setEmail(demoEmail);
    setPassword(demoPassword);
    
    Swal.fire({
      title: 'Demo Credentials Loaded!',
      text: `You can now login as ${role.toUpperCase()}`,
      icon: 'info',
      timer: 1500,
      showConfirmButton: false
    });
  };

  const sendMessage = async () => {
    const message = aiInput.trim();
    if (!message) return;

    setAiInput('');
    setMessages(prev => [...prev, { text: message, sender: 'user' }]);
    setIsTyping(true);

    try {
      const response = await api.post('ai/chat/', {
        message,
        context: { dashboard: 'Login Page', status: 'Guest' }
      });
      setMessages(prev => [...prev, { text: response.data.reply, sender: 'ai' }]);
    } catch (error) {
      console.error('AI Error:', error);
      setMessages(prev => [...prev, { text: "Neural link failed. Try again.", sender: 'ai', error: true }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="login-card" data-aos="zoom-in">
          <div className="row g-0 h-100">
            {/* Left Side - Welcome & Info */}
            <div className="col-lg-5">
              <div className="login-left">
                <div className="mb-5">
                  <span className="text-white text-decoration-none d-flex align-items-center">
                    <i className="bi bi-kanban-fill fs-3 me-2"></i>
                    <span className="fs-3 fw-bold">TaskVision</span>
                  </span>
                </div>

                <h1 className="fw-bold mb-4">Welcome Back</h1>
                <p className="mb-4">
                  Login to access your dashboard and continue managing your workflow.
                </p>

                <div className="mt-4">
                  <h5 className="mb-3">Demo Accounts Available</h5>
                  <div className="demo-account border-0" onClick={() => fillDemoAccount('po')}>
                    <div className="d-flex align-items-center">
                      <div className="role-badge badge-po mb-0">PO</div>
                      <div className="ms-3">
                        <h6 className="mb-0">Product Owner</h6>
                        <p className="text-white-50 mb-0 small">po@taskvision.com / password123</p>
                      </div>
                    </div>
                  </div>

                  <div className="demo-account border-0" onClick={() => fillDemoAccount('pm')}>
                    <div className="d-flex align-items-center">
                      <div className="role-badge badge-pm mb-0">PM</div>
                      <div className="ms-3">
                        <h6 className="mb-0">Project Manager</h6>
                        <p className="text-white-50 mb-0 small">pm@taskvision.com / password123</p>
                      </div>
                    </div>
                  </div>

                  <div className="demo-account border-0" onClick={() => fillDemoAccount('tm')}>
                    <div className="d-flex align-items-center">
                      <div className="role-badge badge-tm mb-0">TM</div>
                      <div className="ms-3">
                        <h6 className="mb-0">Team Member</h6>
                        <p className="text-white-50 mb-0 small">tm1@taskvision.com / password123</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-auto pt-5">
                  <p className="mb-2">New to TaskVision?</p>
                  <button className="btn btn-outline-light" onClick={() => Swal.fire('Registration', 'Account creation is handled by administrators or the main site currently.', 'info')}>
                    <i className="bi bi-person-plus me-2"></i>Create Account
                  </button>
                </div>
              </div>
            </div>

            {/* Right Side - Login Form */}
            <div className="col-lg-7">
              <div className="login-right h-100">
                <h3 className="fw-bold mb-1 text-dark">Login to Dashboard</h3>
                <p className="text-muted mb-4">Enter your credentials to access your role-specific dashboard</p>

                <form onSubmit={handleLogin}>
                  <div className="mb-4 text-start">
                    <label className="form-label text-dark fw-semibold">Email Address *</label>
                    <input 
                      type="email" 
                      className="form-control py-2" 
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Enter your email" 
                      required 
                    />
                  </div>

                  <div className="mb-4 text-start">
                    <label className="form-label text-dark fw-semibold">Password *</label>
                    <div className="password-input-group">
                      <input 
                        type={showPassword ? "text" : "password"}
                        className="form-control py-2" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password" 
                        required 
                      />
                      <button 
                        type="button" 
                        className="password-toggle" 
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        <i className={`bi ${showPassword ? 'bi-eye-slash' : 'bi-eye'}`}></i>
                      </button>
                    </div>
                  </div>

                  <div className="mb-4 text-start">
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" id="rememberMe" />
                      <label className="form-check-label text-muted" htmlFor="rememberMe">
                        Remember me
                      </label>
                    </div>
                  </div>

                  <button type="submit" className="btn btn-login mb-4" disabled={loading}>
                    {loading ? (
                      <span><i className="spinner-border spinner-border-sm me-2"></i>Authenticating...</span>
                    ) : (
                      <span><i className="bi bi-box-arrow-in-right me-2"></i>Login</span>
                    )}
                  </button>

                  <div className="text-center mb-4">
                    <span 
                      className="register-link" 
                      style={{cursor:'pointer'}} 
                      onClick={() => Swal.fire('Forgot Password', 'Please contact your system administrator to reset your password.', 'info')}
                    >
                      Forgot Password?
                    </span>
                  </div>

                  <div className="d-flex align-items-center mb-4">
                    <hr className="flex-grow-1" />
                    <span className="mx-3 text-muted small">OR</span>
                    <hr className="flex-grow-1" />
                  </div>

                  {/* Google Login Placeholder styling */}
                  <div className="text-center mb-4 d-flex justify-content-center">
                     <button type="button" className="btn border rounded-pill px-4 py-2 d-flex align-items-center fw-medium bg-white text-dark w-100 justify-content-center shadow-sm" onClick={() => Swal.fire('Google Auth', 'Use standard login for frontend React integration demonstration.', 'info')}>
                        <i className="bi bi-google text-danger me-2"></i> Sign in with Google
                     </button>
                  </div>

                </form>

              </div>
            </div>
          </div>
        </div>
      </div>

      {/* LeadBot Components */}
      <div className="ai-chat-toggle" onClick={() => setChatVisible(!chatVisible)}>
        <i className="bi bi-robot"></i>
      </div>

      {chatVisible && (
        <div className="ai-chat-container">
          <div className="ai-chat-header">
            <div className="d-flex align-items-center">
              <div className="ai-avatar bg-white text-primary me-2 shadow-sm" style={{ width: '35px', height: '35px' }}>
                <i className="bi bi-robot fs-5" style={{ color: '#a456bf' }}></i>
              </div>
              <div className="text-start">
                <h6 className="mb-0 fw-bold">LeadBot</h6>
                <div className="d-flex align-items-center">
                  <span className="status-dot"></span><small className="opacity-75">Online Now</small>
                </div>
              </div>
            </div>
            <div onClick={() => setChatVisible(false)} style={{ cursor: 'pointer', opacity: 0.8 }}>
              <i className="bi bi-x-lg fs-5"></i>
            </div>
          </div>

          <div className="ai-chat-messages">
            {messages.map((msg, index) => (
              <div className={`chat-row ${msg.sender === 'user' ? 'justify-content-end' : ''}`} key={index}>
                {msg.sender === 'ai' && (
                  <div className="ai-avatar flex-shrink-0"><i className="bi bi-robot"></i></div>
                )}
                <div className={`chat-message ${msg.sender === 'ai' ? 'message-ai' : 'message-user'}`}>
                  {msg.error ? <span className="text-danger fw-bold">{msg.text}</span> : msg.text}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="typing-indicator px-2">
                LeadBot is thinking...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="ai-chat-input">
            <div className="input-group">
              <input 
                type="text" 
                className="form-control border-0 bg-transparent shadow-none" 
                value={aiInput}
                onChange={(e) => setAiInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Reply to LeadBot..." 
              />
              <button 
                className="btn btn-link p-0" 
                onClick={sendMessage} 
                style={{ color: '#a456bf' }}
              >
                <i className="bi bi-lightning-charge-fill fs-4 text-warning"></i>
              </button>
            </div>
          </div>
          <div className="ai-chat-footer">
            We're <i className="bi bi-lightning-fill text-warning"></i> by TaskVision
          </div>
        </div>
      )}
    </div>
  );
};

export default Login;
