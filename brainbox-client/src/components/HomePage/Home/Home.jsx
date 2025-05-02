import React from "react";
import Header from "../Header/Header";
import SideMenu from "../SideMenu/SideMenu";
import Chat from "../Chat/Chat";
import { useChat } from "../../../utils/stateManager/chatContext";
import { useAuth } from "../../../utils/hooks/useAuth";
import { getAudioMessages } from "../../../utils/api/neural";
import styles from "./Home.module.css";

function Home({ handleLogout }) {
  //получаем поле activeService из контекста, а также загруженные сообщения чатов
  const { activeService, loadServerChats } = useChat();

  //получаем имя текущего пользователя
  const { userName } = useAuth();

  const isMounted = React.useRef(false);

  React.useEffect(() => {
    if (!isMounted.current) {
      const fetchMessages = async () => {
        try {
          const messages = await getAudioMessages();
          loadServerChats(messages);
        } catch (error) {
          console.error("Ошибка загрузки сообщений: ", error);
        }
      };
      fetchMessages();
      isMounted.current = true;
    }
  }, [loadServerChats]);

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
