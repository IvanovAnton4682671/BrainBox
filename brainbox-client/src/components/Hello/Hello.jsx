import React from "react";
import styles from "./Hello.module.css";
import { GiBrain } from "react-icons/gi";
import { BsBox2 } from "react-icons/bs";
import RegForm from "./RegForm";
import AuthForm from "./AuthForm";

function Hello() {
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
            <BsBox2 className={styles.box}></BsBox2>
            <GiBrain className={styles.brain}></GiBrain>
          </div>
        </div>
      </div>
      <div className={styles.rightPart}>
        {isSwitched ? (
          <RegForm isAnim={isAnim} handleArrowClick={handleArrowClick} />
        ) : (
          <AuthForm isAnim={isAnim} handleArrowClick={handleArrowClick} />
        )}
      </div>
    </div>
  );
}

export default Hello;
