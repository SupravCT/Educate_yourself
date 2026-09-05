import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Profile() {
  const [stats, setStats] = useState(null);
  const [progress, setProgress] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/progress/me/stats")
      .then((res) => setStats(res.data))
      .catch(() => setError("Failed to load stats"));

    api
      .get("/progress/me")
      .then((res) => setProgress(res.data))
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-2xl mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-4">Your Progress</h1>
      {error && <p className="text-red-500">{error}</p>}
      {stats && (
        <div className="flex gap-6 mb-6">
          <div className="border rounded-lg p-4 flex-1 text-center">
            <p className="text-3xl font-bold">{stats.total_xp}</p>
            <p className="text-gray-500 text-sm">Total XP</p>
          </div>
          <div className="border rounded-lg p-4 flex-1 text-center">
            <p className="text-3xl font-bold">{stats.exercises_completed}</p>
            <p className="text-gray-500 text-sm">Exercises Completed</p>
          </div>
        </div>
      )}
      <h2 className="font-semibold mb-2">Completed Exercises</h2>
      <ul className="flex flex-col gap-2">
        {progress.map((p) => (
          <li key={p.uid} className="border rounded p-3 text-sm">
            +{p.xp_earned} XP · {new Date(p.completed_at).toLocaleDateString()}
          </li>
        ))}
      </ul>
    </div>
  );
}