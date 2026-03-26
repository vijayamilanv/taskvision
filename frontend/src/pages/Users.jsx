import { useState, useEffect } from 'react';
import { Card, Table, Badge, Spinner } from 'react-bootstrap';
import api from '../api';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await api.get('auth/users/');
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center mt-5"><Spinner animation="border" /></div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Users Directory</h2>
        <Badge bg="primary" className="fs-6">{users.length} Total Users</Badge>
      </div>

      <Card className="shadow-sm border-0">
        <Card.Body className="p-0">
          <Table responsive hover className="mb-0">
            <thead className="bg-light">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email / Username</th>
                <th>Role</th>
                <th>Phone</th>
                <th>Info</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>#{user.id}</td>
                  <td className="fw-bold">{user.first_name} {user.last_name}</td>
                  <td>{user.email || user.username}</td>
                  <td>
                    <Badge bg={
                      user.role === 'PO' ? 'danger' :
                      user.role === 'PM' ? 'info' : 'secondary'
                    }>
                        {user.role === 'PO' ? 'Product Owner' : 
                         user.role === 'PM' ? 'Project Manager' : 'Team Member'}
                    </Badge>
                  </td>
                  <td>{user.phone || 'N/A'}</td>
                  <td>
                    <small className="text-muted">
                        {user.role === 'PO' ? user.company || user.industry : ''}
                        {user.role === 'PM' ? user.specialization : ''}
                        {user.role === 'TM' ? user.skills : ''}
                    </small>
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-muted">No users found</td>
                </tr>
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
      
    </div>
  );
};

export default Users;
