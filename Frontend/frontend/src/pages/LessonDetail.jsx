import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/axios";

export default function LessonDetail() {
  const { lessonUid } = useParams();
  const [exercises, setExercises] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get(`/exercises/lesson/${lessonUid}`)
      .then((res) => setExercises(res.data))
      .catch(() => setError("Failed to load exercises"));
  }, [lessonUid]);

  return (
    <div className="max-w-2xl mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-4">Exercises</h1>
      {error && <p className="text-red-500">{error}</p>}
      <div className="flex flex-col gap-3">
        {exercises.map((ex) => (
          <Link
            key={ex.uid}
            to={`/exercises/${ex.uid}`}
            className="border rounded-lg p-4 hover:bg-gray-50"
          >
            <h2 className="font-semibold">{ex.title}</h2>
            <span className="text-xs text-gray-400">
              {ex.difficulty} · {ex.xp_reward} XP
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}