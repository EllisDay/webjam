import './App.css';
import Login from './loginpage.js';
import Register from './register.js';
import Placeholder from './placeholder.js';
import ForgotPassword from './forgot.js';
import { useState } from 'react';



function App() {
  const [page, setPage] = useState("login");
  function goToRegister() {
    setPage("register");
  }

  function goToLogin() {
    setPage("login");
  }

  function goToPlaceholder() {
    setPage("placeholder");
  }

  function goToForgot() {
    setPage("forgot")
  }
  return(
    <>
    {page === "login" && <Login onRegister={goToRegister} onSuccess={goToPlaceholder} onForgot={goToForgot}/>}
    {page === "register" && <Register onLogin={goToLogin} />}
    {page === "placeholder" && <Placeholder/>}
    {page === "forgot" && <ForgotPassword onLogin={goToLogin}/>}
    </>
  )

}

export default App;