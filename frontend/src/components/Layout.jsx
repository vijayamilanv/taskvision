import { Outlet, Link, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Nav, Button } from 'react-bootstrap';

const Layout = () => {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <Container fluid className="p-0 vh-100 d-flex overflow-hidden">
      <div className="bg-dark text-white p-3 d-flex flex-column" style={{ width: '250px' }}>
        <h3 className="mb-4 d-flex align-items-center">
          <i className="bi bi-kanban me-2"></i> TaskVision
        </h3>
        <Nav className="flex-column flex-grow-1 gap-2">
          <Nav.Link as={Link} to="/" className="text-white d-flex align-items-center">
            <i className="bi bi-speedometer2 me-2"></i> Dashboard
          </Nav.Link>
          <Nav.Link as={Link} to="/projects" className="text-white d-flex align-items-center">
            <i className="bi bi-folder me-2"></i> Projects
          </Nav.Link>
          <Nav.Link as={Link} to="/users" className="text-white d-flex align-items-center">
            <i className="bi bi-people me-2"></i> Users
          </Nav.Link>
        </Nav>
        <div className="mt-auto">
          <Button variant="outline-light" className="w-100" onClick={handleLogout}>
            Logout
          </Button>
        </div>
      </div>
      <div className="flex-grow-1 bg-light overflow-auto p-4">
        <Outlet />
      </div>
    </Container>
  );
};

export default Layout;
