import styles from "./Loading.module.css";

function Loading() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.loading}>
        <h3>Пожалуйста, подождите...</h3>
        <img className={styles.eclipse} src="./eclipse.gif" alt="eclipse" />
      </div>
    </div>
  );
}

export default Loading;
