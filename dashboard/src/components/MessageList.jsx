import React, { useState, useEffect, useRef } from "react";
import Message from "./Message";
import styles from "./MessageList.module.css";

function MessageList({ activeThread }) {
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        if (activeThread && activeThread.id > 0) {
            fetch(`/user-messages/threads/${activeThread.id}/`)
                .then(res => res.json())
                .then(data => {
                    setMessages(data);
                    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
                });
        }
    }, [activeThread]);

    return (
        <div className={styles.messageListContainer}>
            {messages.map(m => (
                <Message key={m.id} msg={m} />
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
}

export default MessageList;
