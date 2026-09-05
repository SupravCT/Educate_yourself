import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function AdminCreateLesson() {
  const [form, setForm] = useState({
    title: "",
    description: "",
    topic: "",
    order_index: 1,
    difficulty: "beginner",
    xp_reward: 10,
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === "order_index" || name === "xp_reward" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const res = await api.post("/lessons/", form);
      setSuccess(`Lesson created: ${res.data.title}`);
      setTimeout(() => navigate("/lessons"), 1000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create lesson");
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-4">Create Lesson</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          className="border rounded px-3 py-2"
          name="title"
          placeholder="Title"
          value={form.title}
          onChange={handleChange}
          required
        />
        <textarea
          className="border rounded px-3 py-2"
          name="description"
          placeholder="Description"
          value={form.description}
          onChange={handleChange}
          required
        />
        <input
          className="border rounded px-3 py-2"
          name="topic"
          placeholder="Topic (e.g. python)"
          value={form.topic}
          onChange={handleChange}
          required
        />
        <select
          className="border rounded px-3 py-2"
          name="difficulty"
          value={form.difficulty}
          onChange={handleChange}
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        <input
          className="border rounded px-3 py-2"
          name="order_index"
          type="number"
          placeholder="Order Index"
          value={form.order_index}
          onChange={handleChange}
        />
        <input
          className="border rounded px-3 py-2"
          name="xp_reward"
          type="number"
          placeholder="XP Reward"
          value={form.xp_reward}
          onChange={handleChange}
        />
        {error && <p className="text-red-500 text-sm">{error}</p>}
        {success && <p className="text-green-600 text-sm">{success}</p>}
        <button className="bg-blue-600 text-white rounded py-2 hover:bg-blue-700">
          Create Lesson
        </button>
      </form>
    </div>
  );
}