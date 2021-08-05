import React from "react";
import styles from "./MessageThread.module.css";

function MessageThread({ thread, currentUser, setSelectedThread }) {
    function handleClick(e, thread) {
        setSelectedThread(thread);
    }

    return (
        <div className={styles.thread} onClick={e => handleClick(e, thread)}>
            <img src={thread.created_by.profile_pic} alt={`${thread.created_by.first_name} ${thread.created_by.last_name} Profile Image`} />
            <div className={styles.threadInfo}>
                <p className={styles.threadNames}>
                    {
                        thread.created_by.email === currentUser
                            ? "Me"
                            : <strong>{thread.created_by.first_name} {thread.created_by.last_name}</strong>
                    },&nbsp;
                    {
                        thread.recipient.email === currentUser
                            ? "Me"
                            : <strong>{thread.recipient.first_name} {thread.recipient.last_name}</strong>
                    }
                    <span className={styles.jobTitle}>{thread.job.title}</span>
                </p>
                <p className={styles.threadDescription}>{thread.job.description}</p>
            </div>
        </div>
    );
}

export default MessageThread;
