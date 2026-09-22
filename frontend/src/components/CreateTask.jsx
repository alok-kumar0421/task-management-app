import React, { useState, useEffect } from 'react';
import { fetchUsers, createTask } from '../services/api';

function CreateTask({ user, onTaskCreated }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [assignedTo, setAssignedTo] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const data = await fetchUsers();
        setUsers(data);
        if (data.length > 0) {
          setAssignedTo(data[0].id);
        }
      } catch (error) {
        console.error("Failed to load users", error);
      }
    };
    loadUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !description || !assignedTo) {
      alert("Please fill in all fields.");
      return;
    }

    setLoading(true);
    try {
      await createTask({
        title,
        description,
        assigned_to: assignedTo,
        created_by: user.id
      });
      alert("Task created successfully!");
      setTitle('');
      setDescription('');
      onTaskCreated();
    } catch (error) {
      console.error("Error creating task:", error);
      alert("Failed to create task.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-task-form">
      <h3>Create New Task</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Title</label>
          <input 
            type="text" 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            placeholder="Task Title"
            required 
          />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea 
            value={description} 
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Task Description"
            required 
          />
        </div>
        <div className="form-group">
          <label>Assign To</label>
          <select value={assignedTo} onChange={(e) => setAssignedTo(e.target.value)} required>
            {users.map(u => (
              <option key={u.id} value={u.id}>{u.name} ({u.email})</option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Creating...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
}

export default CreateTask;
