import React, { useState } from "react";
import { useAppContext } from "../context/AppContext"; // Adjust path as needed
import toast from "react-hot-toast";

const Login = () => {
    const [state, setState] = useState("login");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    
    // Destructure from Context
    const { axios, setToken } = useAppContext();

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Logic to determine endpoint and payload
        const url = state === "login" ? "/api/user/login" : "/api/user/register";
        const payload = state === "login" ? { email, password } : { name, email, password };

        try {
            const { data } = await axios.post(url, payload);
            
            if (data.success) {
                setToken(data.token);
                localStorage.setItem('token', data.token);
                toast.success(state === "login" ? "Login successful!" : "Account created!");
            } else {
                toast.error(data.message);
            }
        } catch (error) {
            // Check if axios error has a response message from backend
            const errorMsg = error.response?.data?.message || error.message;
            toast.error(errorMsg);
        }
    };

    return (
        <div className="min-h-[80vh] flex items-center justify-center">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4 m-auto items-start p-8 py-12 w-80 sm:w-[352px] text-gray-500 rounded-lg shadow-xl border border-gray-200 bg-white">
                <p className="text-2xl font-medium m-auto">
                    <span className="text-purple-700">User</span> {state === "login" ? "Login" : "Sign Up"}
                </p>

                {state === "register" && (
                    <div className="w-full">
                        <p>Name</p>
                        <input 
                            onChange={(e) => setName(e.target.value)} 
                            value={name} 
                            placeholder="Full Name" 
                            className="border border-gray-200 rounded w-full p-2 mt-1 outline-purple-700" 
                            type="text" 
                            required 
                        />
                    </div>
                )}

                <div className="w-full">
                    <p>Email</p>
                    <input 
                        onChange={(e) => setEmail(e.target.value)} 
                        value={email} 
                        placeholder="email@example.com" 
                        className="border border-gray-200 rounded w-full p-2 mt-1 outline-purple-700" 
                        type="email" 
                        required 
                    />
                </div>

                <div className="w-full">
                    <p>Password</p>
                    <input 
                        onChange={(e) => setPassword(e.target.value)} 
                        value={password} 
                        placeholder="••••••••" 
                        className="border border-gray-200 rounded w-full p-2 mt-1 outline-purple-700" 
                        type="password" 
                        required 
                    />
                </div>

                <button type='submit' className="bg-purple-700 hover:bg-purple-800 transition-all text-white w-full py-2 rounded-md cursor-pointer mt-2">
                    {state === "register" ? "Create Account" : "Login"}
                </button>

                {state === "register" ? (
                    <p className="text-sm">
                        Already have an account? <span onClick={() => setState("login")} className="text-purple-700 cursor-pointer underline">Login here</span>
                    </p>
                ) : (
                    <p className="text-sm">
                        Create an account? <span onClick={() => setState("register")} className="text-purple-700 cursor-pointer underline">Click here</span>
                    </p>
                )}
            </form>
        </div>
    );
};

export default Login;