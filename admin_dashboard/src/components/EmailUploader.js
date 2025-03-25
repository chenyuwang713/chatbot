import React, { useState } from 'react';
import axios from 'axios';

const EmailUploader = ({ token }) => {
    const [emailList, setEmailList] = useState('');
    
    const handleUploadEmails = async () => {
        try {
            await axios.post('/upload_emails', { emails: emailList.split('\n') }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            alert('Emails uploaded successfully');
            setEmailList('');
        } catch (error) {
            console.error('Failed to upload emails', error);
            alert('Failed to upload emails');
        }
    };

    return (
        <div>
            <h2>Upload Emails</h2>
            <textarea 
                value={emailList} 
                onChange={(e) => setEmailList(e.target.value)}
                placeholder='Enter emails, one per line'
                rows={5}
                cols={50}
            />
            <br/>
            <button onClick={handleUploadEmails}>Upload</button>
        </div>
    );
};

export default EmailUploader;