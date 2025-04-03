import React from "react";
import axios from "axios";
import { FaArrowAltCircleRight } from "react-icons/fa";
import styles from "./Forms.module.css";

function RegForm({ isAnim, handleArrowClick, handleAuthentication }) {
  const [email, setEmail] = React.useState("");
  const [name, setName] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [emailValid, setEmailValid] = React.useState(false);
  const [nameValid, setNameValid] = React.useState(false);
  const [passwordValid, setPasswordValid] = React.useState(false);
  const [emailTouched, setEmailTouched] = React.useState(false);
  const [nameTouched, setNameTouched] = React.useState(false);
  const [passwordTouched, setPasswordTouched] = React.useState(false);

  React.useEffect(() => {
    if (emailTouched) {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      setEmailValid(emailRegex.test(email));
    }
  }, [email, emailTouched]);

  React.useEffect(() => {
    if (nameTouched) {
      const nameRegex = /^[a-zA-Z0-9]{1,20}$/;
      setNameValid(nameRegex.test(name));
    }
  }, [name, nameTouched]);

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
    setNameTouched(true);
    setPasswordTouched(true);

    if (!emailValid || !nameValid || !passwordValid) {
      var alertText = "";

      if (!emailValid) {
        alertText += "\nВведите корректный email-адрес!";
      }

      if (!nameValid) {
        alertText +=
          "\nИмя в системе может состоять из латинских букв и цифр, а также иметь длину от 1 до 20 символов!";
      }

      if (!passwordValid) {
        alertText +=
          "\nПароль должен содержать минимум 1 строчную латинскую букву; 1 заглавную латинскую букву; 1 цифру; 1 специальный знак; быть от 5 до 20 символов!";
      }

      alert(alertText);
      return;
    } else {
      try {
        const response = await axios.post(
          "http://localhost:8001/auth/register",
          {
            email: email,
            name: name,
            password: password,
          }
        );

        if (response.status === 200) {
          handleAuthentication(true);
        } else if (response.status === 202) {
          alert(
            "Пользователь с такими данными уже существует!",
            response.message
          );
          console.log(response.message);
          return;
        }
      } catch (error) {
        alert("Произошла ошибка!");
        console.error("Ошибка при выполнении регистрации: ", error);
      }
    }
  };

  return (
    <div className={styles.formAndBlock}>
      <div className={`${styles.myForm} ${!isAnim ? "" : styles.hideReg}`}>
        <form onSubmit={handleSubmit}>
          <h1>Регистрация</h1>
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
          <h3>Имя</h3>
          <input
            type="text"
            placeholder="Ваше имя в системе"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setNameTouched(true);
            }}
            className={!nameValid && nameTouched ? styles.inputError : ""}
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
          <button type="submit">Зарегистрироваться</button>
        </form>
      </div>
      <div
        className={`${styles.helpBlockRight} ${!isAnim ? "" : styles.hideReg}`}
      >
        <h3>Уже зарегистрировались?</h3>
        <FaArrowAltCircleRight
          className={styles.rightArrow}
          onClick={handleArrowClick}
        />
        <h3>Авторизоваться</h3>
      </div>
    </div>
  );
}

export default RegForm;
