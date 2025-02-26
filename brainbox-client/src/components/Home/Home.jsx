import styles from "./Home.module.css";
import Header from "./Header";
import SideMenu from "./SideMenu";

function Home({ handleAuthentication }) {
  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <Header handleAuthentication={handleAuthentication} />
      </div>
      <div className={styles.homeBody}>
        <div className={styles.sideMenu}>
          <SideMenu />
        </div>
      </div>
    </div>
  );
}

export default Home;
