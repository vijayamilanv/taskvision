import { useState, useEffect } from 'react';
import { Row, Col, Card, Table, Badge, Spinner } from 'react-bootstrap';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import api from '../api';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('dashboard/');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching dashboard data', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center mt-5"><Spinner animation="border" /></div>;
  if (!data) return <div>Failed to load data</div>;

  const STATUS_COLORS = {
    'active': '#0d6efd',
    'pending': '#ffc107',
    'completed': '#198754'
  };

  const PRIORITY_COLORS = {
    'low': '#6c757d',
    'medium': '#0dcaf0',
    'high': '#fd7e14',
    'critical': '#dc3545'
  };

  return (
    <div>
      <h2 className="mb-4">Dashboard Overview</h2>
      
      {/* Summary Cards */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="shadow-sm border-0 text-center">
            <Card.Body>
              <h5 className="text-muted">Total Users</h5>
              <h2 className="text-primary fw-bold">{data.totalUsers}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="shadow-sm border-0 text-center">
            <Card.Body>
              <h5 className="text-muted">Total Projects</h5>
              <h2 className="text-dark fw-bold">{data.totalProjects}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="shadow-sm border-0 text-center">
            <Card.Body>
              <h5 className="text-muted">Completed</h5>
              <h2 className="text-success fw-bold">{data.completedProjects}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="shadow-sm border-0 text-center">
            <Card.Body>
              <h5 className="text-muted">In Progress</h5>
              <h2 className="text-warning fw-bold">{data.inProgressProjects}</h2>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Charts Row */}
      <Row className="mb-4">
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white border-0 fw-bold">Project Status Distribution</Card.Header>
            <Card.Body style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data.projectsByStatus}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="count"
                    nameKey="status"
                    label
                  >
                    {data.projectsByStatus.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={STATUS_COLORS[entry.status.toLowerCase()] || '#8884d8'} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white border-0 fw-bold">Project Priority levels</Card.Header>
            <Card.Body style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.projectsByPriority}>
                  <XAxis dataKey="priority" textAnchor="end" />
                  <YAxis />
                  <Tooltip cursor={{fill: 'transparent'}}/>
                  <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                    {data.projectsByPriority.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PRIORITY_COLORS[entry.priority.toLowerCase()] || '#8884d8'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Recent Projects Table */}
      <Card className="shadow-sm border-0">
        <Card.Header className="bg-white border-0 fw-bold d-flex justify-content-between align-items-center">
          Recent Projects
        </Card.Header>
        <Card.Body className="p-0">
          <Table responsive hover className="mb-0">
            <thead className="bg-light">
              <tr>
                <th>Project Name</th>
                <th>Start Date</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Budget</th>
              </tr>
            </thead>
            <tbody>
              {data.recentProjects.map(project => (
                <tr key={project.id}>
                  <td className="fw-bold">{project.name}</td>
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
                    } text={project.status === 'pending' ? "dark" : "light"}>{project.status.toUpperCase()}</Badge>
                  </td>
                  <td>${project.budget}</td>
                </tr>
              ))}
              {data.recentProjects.length === 0 && (
                <tr>
                  <td colSpan="5" className="text-center py-4 text-muted">No projects found</td>
                </tr>
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
      
    </div>
  );
};

export default Dashboard;
