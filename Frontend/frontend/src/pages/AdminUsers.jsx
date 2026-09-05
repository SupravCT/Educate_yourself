import { useEffect, useState } from "react";
import api from "../api/axios";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  const loadUsers = () => {
    api
      .get("/auth/users")
      .then((res) => setUsers(res.data))
      .catch(() => setError("Failed to load users"));
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const toggleRole = async (user) => {
    const newRole = user.role === "admin" ? "user" : "admin";
    try {
      await api.patch(`/auth/users/${user.uid}/role`, { role: newRole });
      loadUsers();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update role");
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-4">Manage Users</h1>
      {error && <p className="text-red-500 mb-3">{error}</p>}
      <div className="flex flex-col gap-2">
        {users.map((u) => (
          <div key={u.uid} className="border rounded p-3 flex justify-between items-center">
            <div>
              <p className="font-medium">{u.username}</p>
              <p className="text-sm text-gray-500">{u.email}</p>
              <span className="text-xs uppercase text-gray-400">{u.role}</span>
            </div>
            <button
              onClick={() => toggleRole(u)}
              className={`px-3 py-1 rounded text-sm ${
                u.role === "admin"
                  ? "bg-red-100 text-red-700 hover:bg-red-200"
                  : "bg-green-100 text-green-700 hover:bg-green-200"
              }`}
            >
              {u.role === "admin" ? "Demote to User" : "Promote to Admin"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}