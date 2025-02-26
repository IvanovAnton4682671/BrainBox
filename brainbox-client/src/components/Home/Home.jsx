import React from "react";
import styles from "./Home.module.css";
import Header from "./Header";
import SideMenu from "./SideMenu";
import Chat from "./Chat";

function Home({ handleAuthentication }) {
  const [selectedChat, setSelectedChat] = React.useState(false);

  const handleSelectedChat = () => {
    setSelectedChat(true);
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <Header handleAuthentication={handleAuthentication} />
      </div>
      <div className={styles.homeBody}>
        <div className={styles.sideMenu}>
          <SideMenu handleSelectedChat={handleSelectedChat} />
        </div>
        <div className={styles.chat}>
          {!selectedChat ? (
            <h3>Выберите какой-нибудь чат!</h3>
          ) : (
            <Chat />
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
