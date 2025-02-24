import React from "react";
import styles from "./Hello.module.css";
import { GiBrain } from "react-icons/gi";
import { BsBox2 } from "react-icons/bs";
import { FaArrowAltCircleRight } from "react-icons/fa";
import { FaArrowAltCircleLeft } from "react-icons/fa";

function Hello() {
  const [isRegister, setIsRegister] = React.useState(true)
  const handleRightArrowClick = () => {
    setIsRegister(!isRegister)
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.leftPart}>
        <div className={styles.title}>
          <h1>BrainBox</h1>
          <div className={styles.icons}>
            <BsBox2 className={styles.box}></BsBox2>
            <GiBrain className={styles.brain}></GiBrain>
          </div>
        </div>
      </div>
      <div className={styles.rightPart}>

      <div className={styles.formAndBlock}>
          <div className={`${styles.helpBlockLeft} ${!isRegister ? "" : styles.hideAuth}`}>
            <h3>Ещё не зарегистрировались?</h3>
            <FaArrowAltCircleLeft className={styles.leftArrow} onClick={handleRightArrowClick}></FaArrowAltCircleLeft>
            <h3>Зарегистрироваться</h3>
          </div>
          <div className={`${styles.myForm} ${!isRegister ? "" : styles.hideAuth}`}>
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

        <div className={styles.formAndBlock}>
          <div className={`${styles.myForm} ${!isRegister ? styles.hideReg : ""}`}>
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
          <div className={`${styles.helpBlockRight} ${!isRegister ? styles.hideReg : ""}`}>
            <h3>Уже зарегистрировались?</h3>
            <FaArrowAltCircleRight className={styles.rightArrow} onClick={handleRightArrowClick}></FaArrowAltCircleRight>
            <h3>Авторизоваться</h3>
          </div>
        </div>

        

      </div>
    </div>
  );
}

export default Hello;
