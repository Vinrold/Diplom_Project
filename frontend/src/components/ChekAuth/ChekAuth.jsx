export const checkAuth = async (onUser) => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    onUser(null);
    return;
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/users/me', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      onUser(null);
      return;
    }

    const user = await res.json();
    onUser(user);
  } catch {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    onUser(null);
  }
};
