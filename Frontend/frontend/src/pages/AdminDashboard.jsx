import { Link } from "react-router-dom";

export default function AdminDashboard() {
  return (
    <div className="max-w-2xl mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
      <div className="flex flex-col gap-3">
        <Link to="/admin/lessons/new" className="border rounded-lg p-4 hover:bg-gray-50">
          Create Lesson
        </Link>
        <Link to="/admin/exercises/new" className="border rounded-lg p-4 hover:bg-gray-50">
          Create Exercise
        </Link>
        <Link to="/admin/users" className="border rounded-lg p-4 hover:bg-gray-50">
          Manage Users
        </Link>
      </div>
    </div>
  );
}