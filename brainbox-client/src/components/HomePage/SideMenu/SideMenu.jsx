import React from "react";
import { useChat } from "../../../utils/StateManager/ChatContext";
import styles from "./SideMenu.module.css";

//Статический список сервисов вынесен за пределы компонента:
//1. Не зависит от состояния/пропсов
//2. Не будет пересоздаваться при каждом рендере
//3. Легко модифицировать/расширять
const services = [
  { id: "speechToText", label: "Речь в текст" },
  { id: "imageGeneration", label: "Генерация картинок" },
  { id: "chatBot", label: "Чат-бот" },
];

function SideMenu() {
  //получаем метод и поле из контекста
  const { selectService, activeService } = useChat();

  //обработчик клика по элементу меню
  const handleItemClick = (serviceId) => {
    selectService(serviceId); //меняем активный сервис на кликнутый через контекст
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.title}>
        <h4>Список сервисов</h4>
      </div>
      <div className={styles.listOfServices}>
        {services.map((service) => (
          <div
            key={service.id} //уникальный ключ для React-оптимизаций
            className={`${styles.menuItem} ${
              activeService === service.id ? styles.selectedItem : ""
            }`}
            onClick={() => handleItemClick(service.id)}
          >
            {service.label}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SideMenu;
