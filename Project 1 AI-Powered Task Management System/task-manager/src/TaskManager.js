import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './TaskManager.css';

const API = 'http://localhost:5000';

function TaskManager() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState({ title: '', description: '', status: '', priority: '', deadline: '', category: '' });
  const [loading, setLoading] = useState(false);
  const [predicting, setPredicting] = useState(false);
  const [search, setSearch] = useState('');
  const [stats, setStats] = useState(null);
  const [filters, setFilters] = useState({ status: '', priority: '', category: '' });
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchTasks();
    fetchStats();
    fetchCategories();
  }, []);

  // Fetch tasks with filters and search
  const fetchTasks = async () => {
    setLoading(true);
    try {
      let url = `${API}/tasks?`;
      if (filters.status) url += `status=${filters.status}&`;
      if (filters.priority) url += `priority=${filters.priority}&`;
      if (filters.category) url += `category=${filters.category}&`;
      if (search) url += `search=${encodeURIComponent(search)}&`;
      const res = await axios.get(url);
      setTasks(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      setTasks([]);
      alert('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API}/stats`);
      setStats(res.data);
    } catch {}
  };

  const fetchCategories = async () => {
    try {
      const res = await axios.get(`${API}/categories`);
      setCategories(Array.isArray(res.data) ? res.data : []);
    } catch {}
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePredict = async () => {
    if (!form.title || !form.description) return alert('Enter title and description for prediction');
    try {
      setPredicting(true);
      const res = await axios.post(`${API}/predict_category`, {
        title: form.title,
        description: form.description,
      });
      setForm({ ...form, category: res.data.predicted_category });
    } catch (error) {
      alert('Prediction failed.');
    } finally {
      setPredicting(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/tasks`, form);
      setForm({ title: '', description: '', status: '', priority: '', deadline: '', category: '' });
      fetchTasks();
      fetchStats();
      fetchCategories();
    } catch (error) {
      alert('Failed to add task');
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API}/tasks/${id}`);
      fetchTasks();
      fetchStats();
      fetchCategories();
    } catch (error) {
      alert('Failed to delete task');
    }
  };

  const handleSearch = (e) => {
    setSearch(e.target.value);
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleFilterApply = () => {
    fetchTasks();
  };

  const handleExport = async (format = 'csv') => {
    try {
      const res = await axios.get(`${API}/export?format=${format}`);
      if (format === 'csv') {
        const blob = new Blob([res.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'tasks.csv';
        a.click();
      } else {
        // For JSON, just download as .json
        const blob = new Blob([JSON.stringify(res.data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'tasks.json';
        a.click();
      }
    } catch {
      alert('Export failed');
    }
  };

  return (
    <div className="task-manager">
      <h2>📝 AI Task Manager</h2>

      {/* Stats */}
      {stats && (
        <div className="stats">
          <span>Total: {stats.total_tasks}</span>
          <span>Completed: {stats.completed_tasks}</span>
          <span>In Progress: {stats.in_progress_tasks}</span>
          <span>Overdue: {stats.overdue_tasks}</span>
          <span>Due Soon: {stats.due_soon_tasks}</span>
          <span>Completion Rate: {stats.completion_rate}%</span>
        </div>
      )}

      {/* Search and Filters */}
      <div className="filters">
        <input placeholder="Search..." value={search} onChange={handleSearch} />
        <select name="status" value={filters.status} onChange={handleFilterChange}>
          <option value="">All Status</option>
          <option value="todo">Todo</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <select name="priority" value={filters.priority} onChange={handleFilterChange}>
          <option value="">All Priority</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <select name="category" value={filters.category} onChange={handleFilterChange}>
          <option value="">All Categories</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        <button onClick={handleFilterApply}>Apply</button>
        <button onClick={() => { setFilters({ status: '', priority: '', category: '' }); setSearch(''); fetchTasks(); }}>Reset</button>
        <button onClick={() => handleExport('csv')}>Export CSV</button>
        <button onClick={() => handleExport('json')}>Export JSON</button>
      </div>

      {/* Add Task Form */}
      <form className="task-form" onSubmit={handleSubmit}>
        <input name="title" placeholder="Title" value={form.title} onChange={handleChange} required />
        <textarea name="description" placeholder="Description" value={form.description} onChange={handleChange} required />
        <input name="status" placeholder="Status" value={form.status} onChange={handleChange} />
        <input name="priority" placeholder="Priority" value={form.priority} onChange={handleChange} />
        <input name="deadline" placeholder="Deadline" type="date" value={form.deadline} onChange={handleChange} />
        <input name="category" placeholder="Category" value={form.category} onChange={handleChange} readOnly />

        <div className="button-group">
          <button type="button" onClick={handlePredict} disabled={predicting}>
            {predicting ? 'Predicting...' : 'Predict Category'}
          </button>
          <button type="submit">Add Task</button>
        </div>
      </form>

      <hr />

      {/* Task List */}
      <div className="task-list">
        <h3>📋 Tasks ({tasks.length})</h3>
        {loading ? (
          <p>Loading tasks...</p>
        ) : tasks.length === 0 ? (
          <p>No tasks found.</p>
        ) : (
          <ul>
            {tasks.map((t) => (
              <li key={t.id} className="task-item">
                <div>
                  <strong>{t.title}</strong>
                  <p>{t.description}</p>
                  <span className="badge">{t.category}</span>
                  <span className="meta">
                    Status: <b>{t.status}</b> | Priority: <b>{t.priority}</b> | Deadline: <b>{t.deadline}</b>
                  </span>
                </div>
                <button className="delete-btn" onClick={() => handleDelete(t.id)}>❌</button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default TaskManager;
