import React, { useState } from "react";
import MessageThreadList from "./MessageThreadList";
import MessageList from "./MessageList";
import AddMessage from "./AddMessage";
import styles from "./App.module.css";

function App() {
    const [currentUserId, setCurrentUserId] = useState("");
    const [selectedThread, setSelectedThread] = useState({});
    const [refreshMessages, setRefreshMessages] = useState({});

    return (
        <div className={styles.messagesContainer}>
            <MessageThreadList setSelectedThread={setSelectedThread} setCurrentUserId={setCurrentUserId} />
            <MessageList key={refreshMessages} activeThread={selectedThread} />
            {(selectedThread && selectedThread.id > 0) && 
                <AddMessage 
                    selectedThread={selectedThread} 
                    currentUserId={currentUserId}
                    setRefreshMessages={setRefreshMessages}
                />
            }
        </div>
    )
}

export default App
