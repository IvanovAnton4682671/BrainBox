import { GiBrain } from "react-icons/gi";
import { BsBox2 } from "react-icons/bs";
import { IoPersonCircleSharp } from "react-icons/io5";
import styles from "./Header.module.css";

function Header({ handleLogout, userName }) {
  const handleConfirmExit = async () => {
    if (window.confirm("Вы уверены, что хотите выйти из аккаунта?")) {
      const success = await handleLogout();
      if (success) {
        window.location.reload();
      } else {
        alert("Не удалось выйти из системы!");
      }
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.title}>
        <h2>BrainBox</h2>
        <div className={styles.icons}>
          <BsBox2 className={styles.box} />
          <GiBrain className={styles.brain} />
        </div>
      </div>
      <div className={styles.person}>
        <IoPersonCircleSharp className={styles.personIcon} />
        <span className={styles.userName}>Привет, {userName}</span>
        <button
          type="button"
          onClick={handleConfirmExit}
          className={styles.buttonExit}
        >
          Выйти из учётной записи
        </button>
      </div>
    </div>
  );
}

export default Header;
