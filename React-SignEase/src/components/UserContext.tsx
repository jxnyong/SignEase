import React, { createContext, useState, useEffect } from 'react';
import jwtDecode from 'jwt-decode';

interface User {
  username: string;
  fullName: string;
  email: string;
}

interface UserContextProps {
  userLogged: boolean;
  setUserLogged: (value: boolean) => void;
  currentUser: User | null;
  setCurrentUser: (value: User | null) => void;
}

export const UserContext = createContext<UserContextProps>({
  userLogged: false,
  setUserLogged: () => { },
  currentUser: null,
  setCurrentUser: () => { },
});

interface UserProviderProps {
  children: React.ReactNode;
}

export const UserProvider: React.FunctionComponent<UserProviderProps> = ({ children }) => {
  const [userLogged, setUserLogged] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setUserLogged(true);
      const decodedToken = jwtDecode(token) as User;
      setCurrentUser(decodedToken);
    }
  }, []);

  return (
    <UserContext.Provider
      value={{ userLogged, setUserLogged, currentUser, setCurrentUser }}
    >
      {children}
    </UserContext.Provider>
  );
};

