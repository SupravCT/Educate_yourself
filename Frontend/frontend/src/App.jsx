import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminRoute from "./components/AdminRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Lessons from "./pages/Lessons";
import LessonDetail from "./pages/LessonDetail";
import ExerciseDetail from "./pages/ExerciseDetail";
import Profile from "./pages/Profile";
import AdminDashboard from "./pages/AdminDashboard";
import AdminCreateLesson from "./pages/AdminCreateLesson";
import AdminCreateExercise from "./pages/AdminCreateExercise";
import AdminUsers from "./pages/AdminUsers";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
          <Route path="/admin/lessons/new" element={<AdminRoute><AdminCreateLesson /></AdminRoute>} />
          <Route path="/admin/exercises/new" element={<AdminRoute><AdminCreateExercise /></AdminRoute>} />
          <Route path="/admin/users" element={<AdminRoute><AdminUsers /></AdminRoute>} />
          <Route
            path="/lessons"
            element={
              <ProtectedRoute>
                <Lessons />
              </ProtectedRoute>
            }
          />
          <Route
            path="/lessons/:lessonUid"
            element={
              <ProtectedRoute>
                <LessonDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/exercises/:exerciseUid"
            element={
              <ProtectedRoute>
                <ExerciseDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}