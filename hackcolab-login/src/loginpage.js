import './loginpage.css';
import { auth } from "./firebase";
import { signInWithEmailAndPassword } from "firebase/auth";
import { useState } from 'react';

function Login(){
    const [email, setEmail] = useState(""); // state variables with varName, setterFunction
    const [pword, setPword] = useState("");
    const manageLogin = async (e) => { //creates manageLogin function which is asynchronus function, which allows the await keyword w/ promise
        // e.preventDefault();
        try {
            await signInWithEmailAndPassword(auth, email, pword); //attempt signIn function and wait for it to complete
            alert("Login successful!"); // and if it doesn't throw an error we are happy
        } catch (loginError) { //and if it does throw an error we are sad
            alert(loginError.message); // but we send an alert with the message
        }
    };
    return (
        <div className='pageBkg'>
            <form onSubmit={manageLogin} className='loginBlock'>
                <input
                    type="email"
                    value={email}
                    onChange={(emailInput) => setEmail(emailInput.target.value)}
                    placeholder="Enter Email"
                />
                <input
                    type="password"
                    value={pword}
                    onChange={(pwordInput) => setPword(pwordInput.target.value)}
                    placeholder="Enter Password"
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;

