import React from "react";
import styles from "./Message.module.css";

function Message({ msg }) {
    const timestamp = new Intl.DateTimeFormat('en-US', { dateStyle: "medium", timeStyle: "short" }).format(new Date(msg.timestamp));

    return (
        <div className={styles.message}>
            <img src={msg.sender.profile_pic} alt={`${msg.sender.first_name} ${msg.sender.last_name} Profile Image`} />
            <div>
                <p className={styles.messageSender}>
                    {msg.sender.first_name}
                    <span className={styles.messageTimestamp}>
                        {timestamp}
                    </span>
                </p>
                <p className={styles.messageBody}>{msg.message_body}</p>
            </div>
        </div>
    );
}

export default Message;
