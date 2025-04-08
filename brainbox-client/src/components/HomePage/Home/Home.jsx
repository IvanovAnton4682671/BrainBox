import React from "react";
import Header from "../Header/Header";
import SideMenu from "../SideMenu/SideMenu";
import Chat from "../Chat/Chat";
import { useChat } from "../../../utils/stateManager/chatContext";
import { useAuth } from "../../../utils/hooks/useAuth";
import styles from "./Home.module.css";

function Home({ handleLogout }) {
  //получаем поле activeService из контекста
  const { activeService } = useChat();

  //получаем имя текущего пользователя
  const { userName } = useAuth();

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <Header handleLogout={handleLogout} userName={userName} />
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
