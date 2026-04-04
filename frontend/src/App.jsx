import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [token, setToken] = useState(localStorage.getItem('token') || '')
  const [secrets, setSecrets] = useState([])
  const [message, setMessage] = useState('')

  const API_BASE = "http://100.95.70.37:8000"

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(`${API_BASE}/token`, { email, password })
      const newToken = res.data.access_token
      localStorage.setItem('token', newToken)
      setToken(newToken)
      setMessage("Login Successful!")
    } catch (err) {
      setMessage(`Error: ${err.response?.data?.detail || "Login Failed"}`)
    }
  }

  const fetchSecrets = async () => {
    try {
      const res = await axios.get(`${API_BASE}/secrets`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setSecrets(res.data.secrets)
    } catch (err) {
      setMessage("Session expired. Please login again.")
      setToken('')
      localStorage.removeItem('token')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken('')
    setSecrets([])
  }

  if (!token) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900 text-white font-sans">
        <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-96 border border-gray-700">
          <h1 className="text-3xl font-bold mb-6 text-blue-400">Zero-Trust Vault</h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <input type="email" placeholder="Email" className="w-full p-3 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:border-blue-500" value={email} onChange={e => setEmail(e.target.value)} required />
            <input type="password" placeholder="Password" className="w-full p-3 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:border-blue-500" value={password} onChange={e => setPassword(e.target.value)} required />
            <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded transition duration-200">Decrypt & Enter</button>
          </form>
          {message && <p className="mt-4 text-red-400 text-sm">{message}</p>}
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-10 font-sans">
      <div className="flex justify-between items-center mb-10">
        <h1 className="text-3xl font-bold text-blue-400">Security Dashboard</h1>
        <button onClick={handleLogout} className="bg-red-600 px-4 py-2 rounded font-bold">Logout</button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-4">Your Encrypted Secrets</h2>
          <button onClick={fetchSecrets} className="bg-green-600 px-4 py-2 rounded mb-4 w-full">Fetch Data from Secure API</button>
          <ul className="space-y-2">
            {secrets.map((s, i) => (
              <li key={i} className="p-3 bg-gray-700 rounded border-l-4 border-blue-500 font-mono text-sm">{s}</li>
            ))}
          </ul>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 text-gray-400">
          <h2 className="text-xl font-semibold mb-2 text-white">Session Info</h2>
          <p className="break-all text-xs font-mono">JWT: {token}</p>
        </div>
      </div>
    </div>
  )
}

export default App
