import styles from "./Hello.module.css";
import { GiBrain } from "react-icons/gi";
import { BsBox2 } from "react-icons/bs";

function Hello() {
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
        <div className={styles.myForm}>
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
      </div>
    </div>
  );
}

export default Hello;
