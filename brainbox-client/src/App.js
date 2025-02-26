import React from "react";
import Login from "./components/Login/Login";
import Home from "./components/Home/Home";

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);

  const handleAuthentication = (isAuth) => {
    setIsAuthenticated(isAuth);
  };

  return (
    <div>
      {isAuthenticated ? (
        <Home handleAuthentication={handleAuthentication} />
      ) : (
        <Login handleAuthentication={handleAuthentication} />
      )}
    </div>
  );
}

export default App;
