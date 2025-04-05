import React from "react";
import { GiBrain } from "react-icons/gi";
import { BsBox2 } from "react-icons/bs";
import { IoPersonCircleSharp } from "react-icons/io5";
import styles from "./Header.module.css";

function Header({ handleAuthentication }) {
  const handleConfirmExit = () => {
    if (window.confirm("Вы уверены, что хотите выйти из аккаунта?")) {
      handleAuthentication(false);
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
        <button
          type="button"
          /*прокинутый метод из App для выхода из аккаунта*/
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
