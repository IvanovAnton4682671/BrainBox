import React from "react";
import { FaArrowAltCircleLeft } from "react-icons/fa";
import { useAuth } from "../../../utils/hooks/useAuth";
import styles from "./Forms.module.css";

function AuthForm({ isAnim, handleArrowClick }) {
  const { login } = useAuth();

  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [emailValid, setEmailValid] = React.useState(false);
  const [passwordValid, setPasswordValid] = React.useState(false);
  const [emailTouched, setEmailTouched] = React.useState(false);
  const [passwordTouched, setPasswordTouched] = React.useState(false);

  React.useEffect(() => {
    if (emailTouched) {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      setEmailValid(emailRegex.test(email));
    }
  }, [email, emailTouched]);

  React.useEffect(() => {
    if (passwordTouched) {
      const passwordRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{5,20}$/;
      setPasswordValid(passwordRegex.test(password));
    }
  }, [password, passwordTouched]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setEmailTouched(true);
    setPasswordTouched(true);

    if (!emailValid || !passwordValid) {
      var alertText = "";
      if (!emailValid) {
        alertText += "\nВведите корректный email-адрес!";
      }
      if (!passwordValid) {
        alertText +=
          "\nПароль должен содержать минимум 1 строчную латинскую букву; 1 заглавную латинскую букву; 1 цифру; 1 специальный знак; быть от 5 до 20 символов!";
      }

      alert(alertText);
      return;
    }

    const result = await login(email, password);
    if (!result.success) {
      console.error(`Ошибка ${result.error.code}: ${result.error.message}`);
      alert(result.error.message);
    }
  };

  return (
    <div className={styles.formAndBlock}>
      <div
        className={`${styles.helpBlockLeft} ${!isAnim ? styles.hideAuth : ""}`}
      >
        <h3>Ещё не зарегистрировались?</h3>
        <FaArrowAltCircleLeft
          className={styles.leftArrow}
          onClick={handleArrowClick}
        />
        <h3>Зарегистрироваться</h3>
      </div>
      <div className={`${styles.myForm} ${!isAnim ? styles.hideAuth : ""}`}>
        <form onSubmit={handleSubmit}>
          <h1>Авторизация</h1>
          <h3>Почта</h3>
          <input
            type="text"
            placeholder="Ваша актуальная почта"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setEmailTouched(true);
            }}
            className={!emailValid && emailTouched ? styles.inputError : ""}
          ></input>
          <h3>Пароль</h3>
          <input
            type="password"
            placeholder="Ваш сложный пароль"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setPasswordTouched(true);
            }}
            className={
              !passwordValid && passwordTouched ? styles.inputError : ""
            }
          ></input>
          <button type="submit">Авторизоваться</button>
        </form>
      </div>
    </div>
  );
}

export default AuthForm;
