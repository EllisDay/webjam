import './loginreg.css';
import { auth } from "./firebase.js";
import { createUserWithEmailAndPassword} from "firebase/auth";
import { useState } from 'react';

function Register({ onLogin }){
    const [email, setEmail] = useState(""); 
    const [pword, setPword] = useState("");
    async function manageLogin(e){ 
        e.preventDefault();
        try {
            await createUserWithEmailAndPassword(auth, email, pword);
            alert("Creation Succesful!"); 
        } catch (loginError) { 
            alert(loginError.message);
        }
    };
    function setTheEmail(e){
        setEmail(e.target.value);
    };
    function setThePword(e){
        setPword(e.target.value);
    };
    return (
        <div className='pageBkg'>
            <form onSubmit={manageLogin} className='inputBlock'>
                <input
                    className='userInput'
                    type="email"
                    value={email}
                    onChange={setTheEmail}
                    placeholder="Enter Email"
                />
                <input
                    className='userInput'
                    type="password"
                    value={pword}
                    onChange={setThePword}
                    placeholder="Enter Password"
                />
                <button className='userButton'type="submit">Register</button>
                <p className='regLink'>Already have an account? <button onClick={onLogin}>click here</button></p>
            </form>
        </div>
    );
}

export default Register;

