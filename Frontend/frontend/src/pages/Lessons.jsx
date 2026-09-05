import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Lessons() {
  const [lessons, setLessons] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/lessons/")
      .then((res) => setLessons(res.data))
      .catch(() => setError("Failed to load lessons"));
  }, []);

  return (
    <div className="max-w-2xl mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-4">Lessons</h1>
      {error && <p className="text-red-500">{error}</p>}
      <div className="flex flex-col gap-3">
        {lessons.map((lesson) => (
          <Link
            key={lesson.uid}
            to={`/lessons/${lesson.uid}`}
            className="border rounded-lg p-4 hover:bg-gray-50"
          >
            <h2 className="font-semibold">{lesson.title}</h2>
            <p className="text-sm text-gray-600">{lesson.description}</p>
            <span className="text-xs text-gray-400">
              {lesson.topic} · {lesson.difficulty} · {lesson.xp_reward} XP
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}