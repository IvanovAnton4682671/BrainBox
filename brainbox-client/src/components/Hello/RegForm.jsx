import React from "react";
import styles from "./Forms.module.css";
import { FaArrowAltCircleRight } from "react-icons/fa";

function RegForm({ isAnim, isSwitched, handleArrowClick }) {
  return (
    <div className={styles.formAndBlock}>
      <div className={`${styles.myForm} ${!isAnim ? "" : styles.hideReg}`}>
        <form>
          <h1>Регистрация</h1>
          <h3>Почта</h3>
          <input type="email" placeholder="Ваша актуальная почта"></input>
          <h3>Имя</h3>
          <input type="text" placeholder="Ваше имя в системе"></input>
          <h3>Пароль</h3>
          <input type="password" placeholder="Ваш сложный пароль"></input>
          <button type="button">Зарегистрироваться</button>
        </form>
      </div>
      <div
        className={`${styles.helpBlockRight} ${!isAnim ? "" : styles.hideReg}`}
      >
        <h3>Уже зарегистрировались?</h3>
        <FaArrowAltCircleRight
          className={styles.rightArrow}
          onClick={handleArrowClick}
        ></FaArrowAltCircleRight>
        <h3>Авторизоваться</h3>
      </div>
    </div>
  );
}

export default RegForm;
