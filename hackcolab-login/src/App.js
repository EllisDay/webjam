import './App.css';
import Login from './loginpage.js';
import Register from './register.js';
import Placeholder from './placeholder.js';
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
  return(
    <>
    {page === "login" && <Login onRegister={goToRegister} onSuccess={goToPlaceholder} />}
    {page === "register" && <Register onLogin={goToLogin} />}
    {page === "placeholder" && <Placeholder/>}
    </>
  )

}

export default App;