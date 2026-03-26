import { useState, useEffect } from 'react';
import { Card, Table, Badge, Spinner, Form, Row, Col } from 'react-bootstrap';
import api from '../api';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await api.get('projects/');
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredProjects = projects.filter(p => {
    const matchSearch = p.name?.toLowerCase().includes(searchTerm.toLowerCase()) || 
                        p.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchStatus = statusFilter === '' || p.status === statusFilter;
    return matchSearch && matchStatus;
  });

  if (loading) return <div className="text-center mt-5"><Spinner animation="border" /></div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Projects</h2>
        <Badge bg="primary" className="fs-6">{projects.length} Total</Badge>
      </div>

      <Card className="shadow-sm border-0 mb-4 p-3 d-flex flex-row justify-content-between">
            <Form.Group style={{ width: '400px' }}>
              <Form.Control 
                type="text" 
                placeholder="Search projects..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </Form.Group>
            
            <Form.Group style={{ width: '200px' }}>
              <Form.Select 
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="">All Statuses</option>
                <option value="active">In Progress</option>
                <option value="pending">Not Started</option>
                <option value="completed">Completed</option>
              </Form.Select>
            </Form.Group>
      </Card>

      <Card className="shadow-sm border-0">
        <Card.Body className="p-0">
          <Table responsive hover className="mb-0">
            <thead className="bg-light">
              <tr>
                <th>ID</th>
                <th>Project Name</th>
                <th>Description</th>
                <th>Start Date</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Budget</th>
              </tr>
            </thead>
            <tbody>
              {filteredProjects.map(project => (
                <tr key={project.id}>
                  <td>#{project.id}</td>
                  <td className="fw-bold">{project.name}</td>
                  <td><small className="text-muted">{project.description?.substring(0, 50)}...</small></td>
                  <td>{project.start_date || 'N/A'}</td>
                  <td>
                    <Badge bg={
                      project.priority === 'high' ? 'danger' :
                      project.priority === 'medium' ? 'warning' : 'secondary'
                    }>{project.priority.toUpperCase()}</Badge>
                  </td>
                  <td>
                    <Badge bg={
                      project.status === 'completed' ? 'success' :
                      project.status === 'active' ? 'primary' : 'warning'
                    } text={project.status === 'pending' ? 'dark' : 'light'}>
                        {project.status === 'active' ? 'IN PROGRESS' : project.status.toUpperCase().replace('_', ' ')}
                    </Badge>
                  </td>
                  <td>${project.budget}</td>
                </tr>
              ))}
              {filteredProjects.length === 0 && (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">No projects found matching filter</td>
                </tr>
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
      
    </div>
  );
};

export default Projects;
