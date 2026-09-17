import AppRoutes from './routes/AppRoutes'

function App() {
  return (
    <div className="app-container">
      <header style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <h1>Веб-Приложение</h1>
      </header>
      <main style={{ padding: '2rem' }}>
        {}
        <AppRoutes />
      </main>
    </div>
  )
}

export default App