import React from "react";
import RegForm from "../Forms/RegForm";
import AuthForm from "../Forms/AuthForm";
import { GiBrain } from "react-icons/gi";
import { BsBox2 } from "react-icons/bs";
import styles from "./Login.module.css";

function Login({ handleAuthentication }) {
  const [isSwitched, setIsSwitched] = React.useState(true);
  const [isAnim, setIsAnim] = React.useState(false);

  const handleArrowClick = () => {
    setIsAnim(!isAnim);
    setTimeout(() => {
      setIsSwitched(!isSwitched);
    }, 300);
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.leftPart}>
        <div className={styles.title}>
          <h1>BrainBox</h1>
          <div className={styles.icons}>
            <BsBox2 className={styles.box} />
            <GiBrain className={styles.brain} />
          </div>
        </div>
      </div>
      <div className={styles.rightPart}>
        {isSwitched ? (
          <RegForm
            isAnim={isAnim}
            handleArrowClick={handleArrowClick}
            handleAuthentication={handleAuthentication}
          />
        ) : (
          <AuthForm
            isAnim={isAnim}
            handleArrowClick={handleArrowClick}
            handleAuthentication={handleAuthentication}
          />
        )}
      </div>
    </div>
  );
}

export default Login;
