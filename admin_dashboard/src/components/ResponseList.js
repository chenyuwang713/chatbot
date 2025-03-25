import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ResponseList = ({ token }) => {
    const [responses, setResponses] = useState([]);

    useEffect(() => {
        fetchResponses();
    }, []);

    const fetchResponses = async () => {
        try {
            const response = await axios.get('/get_all_responses', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setResponses(response.data.responses);
        } catch (error) {
            console.error('Failed to fetch responses', error);
            alert('Failed to fetch responses');
        }
    };

    return (
        <div>
            <h2>User Responses</h2>
            {responses.length === 0 ? (
                <p>No responses yet.</p>
            ) : (
                <ul>
                    {responses.map((res, index) => (
                        <li key={index}><strong>User {res.user_id}:</strong> {res.question} - {res.answer}</li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default ResponseList;