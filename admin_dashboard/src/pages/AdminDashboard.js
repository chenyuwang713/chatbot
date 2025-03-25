import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const AdminDashboard = () => {
    const [error, setError] = useState("");
    const [responses, setResponses] = useState([]);
    const [emailList, setEmailList] = useState("");
    const [uploadedUsers, setUploadedUsers] = useState([]);
    const [uploadMessage, setUploadMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("admin_token");

        if (!token) {
            navigate("/admin/login"); // Redirect if no token is found
            return;
        }

        //fetchResponses(token);
        fetchUploadedEmails(token); // Fetch uploaded emails on page load
    }, [navigate]);

    const handleLogout = () => {
        localStorage.clear(); // Clear all cached data
        sessionStorage.clear(); // Clear session data
        window.location.href = "/admin/login"; // Redirect to login page
    };


    // const fetchResponses = async (token) => {
    //     try {
    //         const response = await axios.get("http://localhost:5001/get_all_responses", {
    //             headers: { Authorization: `Bearer ${token}` },
    //         });
    //         setResponses(response.data.responses || []);
    //     } catch (error) {
    //         setError("Failed to fetch responses");
    //         console.error("Error fetching responses:", error);
    //     }
    // };

    const handleDeleteUser = async (identifier) => {
        if (!window.confirm("Are you sure you want to delete this user?")) return;
    
        try {
            const response = await fetch(`http://localhost:5001/delete_user?uid=${identifier}`, {
                method: "DELETE",
            });
    
            if (response.ok) {
                setUploadedUsers(prevUsers => prevUsers.filter(user => user.identifier !== identifier));
            } else {
                alert("Failed to delete user. Please try again.");
            }
        } catch (error) {
            console.error("Error deleting user:", error);
            alert("Error deleting user.");
        }
    };

    const fetchUploadedEmails = async (token) => {
        try {
            const response = await axios.get("http://localhost:5001/get_uploaded_emails", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const usersWithLinks = (response.data.users || []).map(user => ({
                ...user,
                surveyLink: `http://localhost:8080/?uid=${user.identifier}` // Ensure survey link is generated
            }));
            
            setUploadedUsers(usersWithLinks);
        } catch (error) {
            console.error("Error fetching uploaded emails:", error);
        }
    };


    const handleUploadEmails = async () => {
        const emails = emailList.split("\n").map(email => email.trim()).filter(email => email);

        if (emails.length === 0) {
            setUploadMessage("No valid emails provided.");
            return;
        }

        const users = emails.map(email => ({
            email,
            identifier: Math.random().toString(36).substring(2, 10) // Generate unique identifier without crypto
        }));

        const updatedUsers = users.map(user => ({
            ...user,
            surveyLink: `http://localhost:8080/?uid=${user.identifier}` // Generate survey link
        }));

        try {
            await axios.post("http://localhost:5001/upload_emails", { users }, {
                headers: { Authorization: `Bearer ${localStorage.getItem("admin_token")}` },
            });

            setUploadMessage("Emails uploaded successfully!");
            setUploadedUsers(prevUsers => [...prevUsers, ...updatedUsers]); // Append new users to existing list
            setEmailList(""); // Clear input after success
        } catch (error) {
            setUploadMessage("Failed to upload emails.");
            console.error("Email upload error:", error);
        }
    };

    return (
        <div style={{ maxWidth: "900px", margin: "auto", padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
                <h1 style={{ margin: 0 }}>Admin Dashboard</h1>
                <button onClick={handleLogout} style={{
                    padding: "10px 15px", backgroundColor: "#d9534f", color: "white",
                    border: "none", borderRadius: "5px", cursor: "pointer", fontSize: "14px"
                }}>
                    Logout
                </button>
            </div>

            <div style={{ backgroundColor: "#ffffff", padding: "20px", borderRadius: "8px", boxShadow: "0 2px 5px rgba(0,0,0,0.1)", marginBottom: "20px" }}>
                <h2>Upload Emails</h2>
                <textarea value={emailList} onChange={(e) => setEmailList(e.target.value)}
                    placeholder="Enter emails, one per line" rows={5} cols={50}
                    style={{ width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc", fontSize: "14px" }}
                />
                <br />
                <button onClick={handleUploadEmails} style={{
                    marginTop: "10px", padding: "10px 15px", backgroundColor: "#0078D4",
                    color: "white", border: "none", borderRadius: "5px", cursor: "pointer", fontSize: "14px"
                }}>
                    Upload Emails
                </button>
                {uploadMessage && <p style={{ color: "green", marginTop: "10px" }}>{uploadMessage}</p>}
            </div>

            <div style={{ backgroundColor: "#ffffff", padding: "20px", borderRadius: "8px", boxShadow: "0 2px 5px rgba(0,0,0,0.1)", marginBottom: "20px" }}>
                <h2>Uploaded Emails</h2>
                {uploadedUsers.length === 0 ? (
                    <p>No emails uploaded yet.</p>
                ) : (
                    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "10px" }}>
                        <thead>
                            <tr style={{ backgroundColor: "#0078D4", color: "white", textAlign: "left" }}>
                                <th style={{ padding: "10px", border: "1px solid #ddd" }}>Email</th>
                                <th style={{ padding: "10px", border: "1px solid #ddd" }}>Unique Identifier</th>
                                <th style={{ padding: "10px", border: "1px solid #ddd" }}>Survey Link</th>
                                <th style={{ padding: "10px", border: "1px solid #ddd" }}>Action</th>
                            </tr> 
                        </thead>
                        <tbody>
                            {uploadedUsers.map((user, index) => (
                                <tr key={index} style={{ backgroundColor: index % 2 === 0 ? "#f8f9fa" : "#ffffff" }}>
                                    <td style={{ padding: "10px", border: "1px solid #ddd" }}>{user.email}</td>
                                    <td style={{ padding: "10px", border: "1px solid #ddd" }}>{user.identifier}</td>
                                    <td style={{ padding: "10px", border: "1px solid #ddd" }}>
                                        <a href={user.surveyLink} target="_blank" rel="noopener noreferrer" style={{ color: "#0078D4", textDecoration: "none" }}>
                                            {user.surveyLink}
                                        </a>
                                    </td>
                                    <td>
                                        <button 
                                            onClick={() => handleDeleteUser(user.identifier)} 
                                            style={{
                                                backgroundColor: "#d9534f", 
                                                color: "white", 
                                                border: "none", 
                                                padding: "5px 10px", 
                                                borderRadius: "5px", 
                                                cursor: "pointer"
                                            }}>
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>

        </div>
    );
};

export default AdminDashboard;