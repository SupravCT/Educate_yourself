import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Editor from "@monaco-editor/react";
import api from "../api/axios";

export default function ExerciseDetail() {
  const { exerciseUid } = useParams();
  const [exercise, setExercise] = useState(null);
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [hint, setHint] = useState("");
  const [question, setQuestion] = useState("");
  const [loadingHint, setLoadingHint] = useState(false);
  const [error, setError] = useState("");

  // NEW — for the Run button
  const [runOutput, setRunOutput] = useState(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    api
      .get(`/exercises/${exerciseUid}`)
      .then((res) => {
        setExercise(res.data);
        setCode(res.data.starter_code);
      })
      .catch(() => setError("Failed to load exercise"));
  }, [exerciseUid]);

  // NEW — run without grading
  const handleRun = async () => {
    setRunning(true);
    setError("");
    setRunOutput(null);
    try {
      const res = await api.post("/submissions/run", {
        exercise_uid: exerciseUid,
        submitted_code: code,
      });
      setRunOutput(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Run failed");
    } finally {
      setRunning(false);
    }
  };

  const handleSubmit = async () => {
    setError("");
    try {
      const res = await api.post("/submissions/", {
        exercise_uid: exerciseUid,
        submitted_code: code,
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Submission failed");
    }
  };

  const handleHint = async () => {
    if (!question.trim()) return;
    setLoadingHint(true);
    setError("");
    try {
      const res = await api.post("/hints/", {
        exercise_uid: exerciseUid,
        user_question: question,
        user_code: code,
      });
      setHint(res.data.hint);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to get hint");
    } finally {
      setLoadingHint(false);
    }
  };

  if (!exercise) return <p className="text-center mt-10">Loading...</p>;

  return (
    <div className="max-w-3xl mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-2">{exercise.title}</h1>
      <p className="text-gray-700 mb-4">{exercise.prompt}</p>

      <div className="border rounded overflow-hidden">
        <Editor
          height="300px"
          defaultLanguage="python"
          value={code}
          onChange={(value) => setCode(value ?? "")}
          theme="vs-dark"
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
          }}
        />
      </div>

      <div className="flex gap-3 mt-3">
        {/* NEW — Run button */}
        <button
          onClick={handleRun}
          disabled={running}
          className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800 disabled:opacity-50"
        >
          {running ? "Running..." : "Run"}
        </button>
        <button
          onClick={handleSubmit}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Submit
        </button>
      </div>

      {/* NEW — run output panel */}
      {runOutput && (
        <div className="mt-4 bg-gray-900 text-green-400 font-mono text-sm p-3 rounded whitespace-pre-wrap">
          {runOutput.stdout || "(no output)"}
          {runOutput.stderr && (
            <div className="text-red-400 mt-2">{runOutput.stderr}</div>
          )}
        </div>
      )}

      {result && (
        <div
          className={`mt-4 p-3 rounded ${
            result.is_correct ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
          }`}
        >
          {result.message} {result.is_correct && `(+${result.xp_awarded} XP)`}
        </div>
      )}

      <div className="mt-8 border-t pt-4">
        <h2 className="font-semibold mb-2">Need a hint?</h2>
        <div className="flex gap-2">
          <input
            className="flex-1 border rounded px-3 py-2"
            placeholder="Ask a question about this exercise..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button
            onClick={handleHint}
            disabled={loadingHint}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loadingHint ? "Thinking..." : "Ask"}
          </button>
        </div>
        {hint && <p className="mt-3 bg-blue-50 p-3 rounded text-sm">{hint}</p>}
      </div>

      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  );
}