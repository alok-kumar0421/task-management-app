import React, { useState, useEffect } from 'react';
import { fetchTasks, completeTask } from '../services/api';
import CreateTask from '../components/CreateTask';

function Dashboard({ user, onLogout }) {
  const [tasks, setTasks] = useState([]);
  const [showCreate, setShowCreate] = useState(false);

  const loadTasks = async () => {
    try {
      const data = await fetchTasks(user.id);
      setTasks(data);
    } catch (error) {
      console.error("Failed to fetch tasks", error);
    }
  };

  useEffect(() => {
    if (user) {
      loadTasks();
    }
  }, [user]);

  const handleComplete = async (taskId) => {
    try {
      await completeTask(taskId, user.id);
      loadTasks(); // reload tasks
    } catch (error) {
      console.error("Failed to complete task", error);
      alert(error.response?.data?.error || "Failed to complete task");
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h2>Welcome, {user.name}</h2>
          <p>{user.email}</p>
        </div>
        <div>
          <button className="btn btn-primary" onClick={() => setShowCreate(!showCreate)}>
            {showCreate ? 'Close' : 'Create Task'}
          </button>
          <button className="btn btn-secondary" onClick={onLogout} style={{ marginLeft: '10px' }}>
            Logout
          </button>
        </div>
      </header>

      {showCreate && (
        <CreateTask user={user} onTaskCreated={() => {
          setShowCreate(false);
          loadTasks();
        }} />
      )}

      <div className="tasks-container">
        <h3>Your Tasks</h3>
        {tasks.length === 0 ? (
          <p>No tasks found.</p>
        ) : (
          <div className="tasks-grid">
            {tasks.map(task => (
              <div key={task.id} className={`task-card ${task.status.toLowerCase()}`}>
                <h4>{task.title}</h4>
                <p className="task-desc">{task.description}</p>
                <div className="task-meta">
                  <span><strong>Status:</strong> {task.status}</span>
                  <span><strong>Created by:</strong> {task.created_by?.name || 'Unknown'}</span>
                  <span><strong>Assigned to:</strong> {task.assigned_to?.name || 'Unknown'}</span>
                </div>
                {task.status === 'Pending' && task.assigned_to?.id === user.id && (
                  <button className="btn btn-success" onClick={() => handleComplete(task.id)}>
                    Mark as Completed
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
