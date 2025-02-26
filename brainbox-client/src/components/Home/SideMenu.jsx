import styles from "./SideMenu.module.css";

function SideMenu() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.title}>
        <h4>Список сервисов</h4>
      </div>
      <div className={styles.listOfServices}>
        <div className={styles.menuItem}>Речь в текст</div>
        <div className={styles.menuItem}>Генерация картинок</div>
      </div>
    </div>
  );
}

export default SideMenu;
