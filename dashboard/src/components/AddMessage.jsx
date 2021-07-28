import React, { useState } from "react";
import SendIcon from '@material-ui/icons/Send';
import styles from "./AddMessage.module.css";

function AddMessage({ selectedThread, currentUserId, setRefreshMessages }) {
    const [newMessage, setNewMessage] = useState("");

    function submitForm(e) {
        e.preventDefault();
        const csrftoken = getCookie("csrftoken");

        const data = {
            sender: currentUserId,
            recipient: currentUserId === selectedThread.recipient.id ? selectedThread.created_by.id : selectedThread.recipient.id,
            message: newMessage,
            thread: selectedThread.id
        };

        fetch("/user-messages/threads/submit-new-message/", {
            credentials: "include",
            method: "POST",
            mode: "same-origin",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            setRefreshMessages(Date.now());
        })

        setNewMessage("");
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    

    return (
        <div className={styles.addMessageContainer}>
            <form className={styles.addMessageForm} onSubmit={submitForm}>
                <input type="hidden" name="csrfmiddlewaretoken" value={getCookie("csrftoken")} />
                <input
                    id="messageTextbox"
                    type="text"
                    placeholder="Send a new message"
                    onChange={e => setNewMessage(e.target.value)}
                    value={newMessage} 
                />
                <button type="submit">
                    <SendIcon style={{ color: "#4B5563" }} />
                </button>
            </form>
        </div>
    );
}

export default AddMessage;
