import AppRoutes from './routes/AppRoutes';
import style from './index.module.css';
import logo from './assets/in-yn.jpeg'


function App() {
  return (
    <div className={style.container}>
      <header className={style.header}>
        <img src={logo} alt="Логотип" className={style.logo}/>
      </header>
      <main className={style.main}>
        <AppRoutes />
      </main>
    </div>
  )
}

export default App