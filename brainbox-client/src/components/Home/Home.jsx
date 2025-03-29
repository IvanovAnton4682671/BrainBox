import React from "react";
import Header from "./Header";
import SideMenu from "./SideMenu";
import Chat from "./Chat";
import { useChat } from "../../utils/ChatContext";
import styles from "./Home.module.css";

function Home({ handleAuthentication }) {
  //получаем поле activeService из контекста
  const { activeService } = useChat();

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <Header handleAuthentication={handleAuthentication} />
      </div>
      <div className={styles.homeBody}>
        <div className={styles.sideMenu}>
          <SideMenu />
        </div>
        <div className={styles.chat}>
          {/*по текущем активному сервису рендерим или предупреждение (если activeService = null), или выбранный сервис*/}
          {!activeService ? (
            <div className={styles.baseInfo}>
              <h3>Выберите какой-нибудь сервис!</h3>
            </div>
          ) : (
            <Chat />
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
