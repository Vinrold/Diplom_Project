import { Navigate, replace, useLocation } from "react-router-dom";

function ProtectedRoute({ children }) {
    const token = localStorage.getItem('access_token');
    const location = useLocation();

    if (!token) {
        return <Navigate to = "/login" state={{ from: location }} replace />
    }
    return children;
}

export default ProtectedRoute;