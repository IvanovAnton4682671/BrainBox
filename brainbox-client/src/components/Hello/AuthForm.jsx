import React from "react";
import styles from "./Forms.module.css";
import { FaArrowAltCircleLeft } from "react-icons/fa";

function AuthForm({ isAnim, isSwitched, handleArrowClick }) {
  return (
    <div className={styles.formAndBlock}>
      <div
        className={`${styles.helpBlockLeft} ${!isAnim ? styles.hideAuth : ""}`}
      >
        <h3>Ещё не зарегистрировались?</h3>
        <FaArrowAltCircleLeft
          className={styles.leftArrow}
          onClick={handleArrowClick}
        ></FaArrowAltCircleLeft>
        <h3>Зарегистрироваться</h3>
      </div>
      <div className={`${styles.myForm} ${!isAnim ? styles.hideAuth : ""}`}>
        <form>
          <h1>Авторизация</h1>
          <h3>Почта</h3>
          <input type="email" placeholder="Ваша актуальная почта"></input>
          <h3>Пароль</h3>
          <input type="password" placeholder="Ваш сложный пароль"></input>
          <button type="button">Авторизоваться</button>
        </form>
      </div>
    </div>
  );
}

export default AuthForm;
