import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function AdminRoute({ children }) {
  const { isAdmin, isLoggedIn } = useAuth();
  if (!isLoggedIn) return <Navigate to="/login" />;
  if (!isAdmin) return <Navigate to="/lessons" />;
  return children;
}