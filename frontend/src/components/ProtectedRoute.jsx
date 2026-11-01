import { Navigate, replace, useLocation } from "react-router-dom";

function ProtectedRoute({ children, isLoggedIn}) {
    const token = localStorage.getItem('access_token');
    const location = useLocation();

    if (!isLoggedIn) {
        return <Navigate to = "/login" state={{ from: location }} replace />
    }
    return children;
}

export default ProtectedRoute;