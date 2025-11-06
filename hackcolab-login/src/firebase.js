// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth"; 
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD1u982tG80HNd3rbxUNSwrvhtgzF1Y-Ws",
  authDomain: "hackcolab-693eb.firebaseapp.com",
  projectId: "hackcolab-693eb",
  storageBucket: "hackcolab-693eb.firebasestorage.app",
  messagingSenderId: "119334542379",
  appId: "1:119334542379:web:589719a43139614893de6e"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);