import React, { useEffect, useState } from "react";
import MessageThread from "./MessageThread";
import styles from "./MessageThreadList.module.css";

function MessageThreadList({ setSelectedThread, setCurrentUserId }) {
    const [currentUser, setCurrentUser] = useState([]);
    const [messageThreads, setMessageThreads] = useState([]);

    useEffect(() => {
        fetch("/user-messages/threads/")
            .then(res => res.json())
            .then(data => {
                setCurrentUser(data.current_user);
                setCurrentUserId(data.current_user_id);
                setMessageThreads(data.message_threads);
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
