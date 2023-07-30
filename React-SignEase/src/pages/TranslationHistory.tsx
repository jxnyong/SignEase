import axios from 'axios';
import React, { useState, useEffect } from 'react';
import ChatBubble from '../components/ChatBubble';
import Breadcrumb from '../components/Breadcrumb';

interface Translation {
  _id: string,
  conversation: string,
  userId: number,
  username: string,
  sessionId: number,
  timestamp: string
}

const TranslationHistory = () => {
  const [translations, setTranslations] = useState<Translation[]>([]);
  const username = localStorage.getItem('username');

  useEffect(() => {
    axios.get('http://localhost:5000/translations', { params: { username } }) // pass the username as a query parameter
      .then(response => {
        console.log(response.data);  // debug output
        setTranslations(JSON.parse(response.data));
      });
  }, [username]);

  return (
    <>
      <div className="mx-auto max-w-270">
        <Breadcrumb pageName="TranslationHistory" />

        <div className="mx-auto max-w-270">
          <div className="grid grid-cols-1 gap-8">
            {translations.map((translation) => (
              <ChatBubble
                key={translation._id}
                username={translation.username}
                timestamp={translation.timestamp}
                message={translation.conversation}
              />
            ))}
          </div>
        </div>

      </div>
    </>
  );
};

export default TranslationHistory;
