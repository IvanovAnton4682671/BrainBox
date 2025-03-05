import React from "react";
import styles from "./SideMenu.module.css";

function SideMenu({ handleSelectedChat }) {
  const [selectedItem, setSelectedItem] = React.useState(null);

  const handleItemClick = (index) => {
    setSelectedItem(index);
    handleSelectedChat();
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.title}>
        <h4>Список сервисов</h4>
      </div>
      <div className={styles.listOfServices}>
        {["Генерация картинок", "Речь в текст", "Чат-бот"].map(
          (item, index) => (
            <div
              key={index}
              className={`${styles.menuItem} ${
                selectedItem === index ? styles.selectedItem : ""
              }`}
              onClick={() => handleItemClick(index)}
            >
              {item}
            </div>
          )
        )}
      </div>
    </div>
  );
}

export default SideMenu;
