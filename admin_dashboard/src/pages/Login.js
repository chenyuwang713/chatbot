import React, { useState } from "react";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");


    const handleLogin = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch("http://localhost:5001/admin/login", {
                method: "POST",
                mode: "cors",  // Ensures CORS headers are respected
                credentials: "include", // Allows sending credentials if needed
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ email, password }),
            });
    
            const data = await response.json();
            if (data.access_token) {
                localStorage.setItem("admin_token", data.access_token);
                window.location.href = "http://localhost:3001/dashboard";
            } else {
                setError("Invalid credentials. Please try again.");
            }
        } catch (error) {
            setError("Network error. Please try again.");
            console.error("Login request failed:", error);
        }
    };

    return (
        <div className="container">
            <h2>Admin Login</h2>
            <form onSubmit={handleLogin}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );
};

export default Login;