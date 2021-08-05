import React, { useEffect, useState } from "react";
import MessageThread from "./MessageThread";
import styles from "./MessageThreadList.module.css";

function MessageThreadList({ selectedJob, sender, setSelectedThread, setCurrentUserId }) {
    const [currentUser, setCurrentUser] = useState([]);
    const [messageThreads, setMessageThreads] = useState([]);

    useEffect(() => {
        let url = "/user-messages/threads/";

        if (selectedJob !== null && selectedJob !== "") {
            url += `?job-id=${selectedJob}`;
        }

        if (sender !== null && sender !== "") {
            url += `&sender=${sender}`;
        }

        fetch(url)
            .then(res => res.json())
            .then(data => {
                setCurrentUser(data.current_user);
                setCurrentUserId(data.current_user_id);
                setMessageThreads(data.message_threads);

                if (data.message_threads.length === 1) {
                    setSelectedThread(data.message_threads[0]);
                }
            });
    }, []);

    return (
        <div className={styles.messageThreadContainer}>
            <h2>All Messages</h2>
            <div className={styles.messageThreadList}>
                {messageThreads.map(t => (
                    <MessageThread 
                        key={t.id}
                        currentUser={currentUser}
                        thread={t}
                        setSelectedThread={setSelectedThread} />
                ))}
            </div>
        </div>
    );
}

export default MessageThreadList
