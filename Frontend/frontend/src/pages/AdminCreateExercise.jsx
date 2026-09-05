import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function AdminCreateExercise() {
  const [lessons, setLessons] = useState([]);
  const [form, setForm] = useState({
    lesson_uid: "",
    title: "",
    prompt: "",
    starter_code: "",
    solution_code: "",
    test_code: "",
    expected_output: "",
    order_index: 1,
    xp_reward: 5,
    difficulty: "beginner",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/lessons/").then((res) => setLessons(res.data));
  }, []);

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
      const res = await api.post("/exercises/", form);
      setSuccess(`Exercise created: ${res.data.title}`);
      setTimeout(() => navigate("/lessons"), 1000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create exercise");
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-4">Create Exercise</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <select
          className="border rounded px-3 py-2"
          name="lesson_uid"
          value={form.lesson_uid}
          onChange={handleChange}
          required
        >
          <option value="">Select a lesson</option>
          {lessons.map((l) => (
            <option key={l.uid} value={l.uid}>
              {l.title}
            </option>
          ))}
        </select>
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
          name="prompt"
          placeholder="Prompt"
          value={form.prompt}
          onChange={handleChange}
          required
        />
        <textarea
          className="border rounded px-3 py-2 font-mono text-sm"
          name="starter_code"
          placeholder="Starter code"
          value={form.starter_code}
          onChange={handleChange}
          required
        />
        <textarea
          className="border rounded px-3 py-2 font-mono text-sm"
          name="solution_code"
          placeholder="Solution code"
          value={form.solution_code}
          onChange={handleChange}
          required
        />
        <textarea
          className="border rounded px-3 py-2 font-mono text-sm"
          name="test_code"
          placeholder="Test code (e.g. print(add(2, 3)))"
          value={form.test_code}
          onChange={handleChange}
          required
        />
        <input
          className="border rounded px-3 py-2 font-mono text-sm"
          name="expected_output"
          placeholder="Expected output (e.g. 5)"
          value={form.expected_output}
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
          Create Exercise
        </button>
      </form>
    </div>
  );
}