import React from 'react';

interface BubbleProps {
    username: string,
    timestamp: string,
    message: string
}

const ChatBubble: React.FC<BubbleProps> = ({ username, timestamp, message }) => {
    return (
        <div style={{ 
                borderRadius: '15px',
                backgroundColor: 'lightgrey',
                marginBottom: '10px',
                width: '100%',
                color: 'black',
                padding: '10px',
                display: 'flex',
                flexDirection: 'column'
            }}>
            <div style={{ fontWeight: 'bold' }}>{username}</div>
            <div>{message}</div>
            <div style={{ fontSize: 'small', alignSelf: 'flex-end' }}>{timestamp}</div>
        </div>
    );
};

export default ChatBubble;
