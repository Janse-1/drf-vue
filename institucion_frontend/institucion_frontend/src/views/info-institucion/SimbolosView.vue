<template>
  <HeaderPublic />
  <div class="simbolos-view">
    <div class="simbolos-header">
      <h1>Símbolos, Castas y Tribus Wayúu</h1>
    </div>
    <section class="simbolos-section">
      <h2>Símbolos de la Etnia Wayúu</h2>
      <div class="simbolos-grid">
        <div class="simbolo-item">
          <img src="@/assets/images/mochila-wayuu.jpeg" alt="Mochila Wayúu" />
          <h3>Mochila Wayúu</h3>
          <p>La mochila es un símbolo de identidad y tradición, tejida a mano por las mujeres Wayúu, representa la creatividad, la paciencia y la transmisión de saberes ancestrales.</p>
          <a href="https://artesaniasdecolombia.com.co/PortalAC/Noticia/la-mochila-wayu-parte-de-la-tradicion-de-colombia_5070" target="_blank" class="more-info">Conoce más aquí</a>
        </div>
        <div class="simbolo-item">
          <img src="@/assets/images/mantas-wayuu.jpg" alt="Manta Wayúu" />
          <h3>Manta Wayúu</h3>
          <p>La manta es la vestimenta tradicional, símbolo de respeto y pertenencia, utilizada en ceremonias y celebraciones importantes.</p>
          <a href="https://www.panoramacultural.com.co/moda/7920/la-manta-wayuu-de-vestido-tradicional-a-tendencia-nacional-y-caribena" target="_blank" class="more-info">Conoce más aquí</a>
        </div>
        <div class="simbolo-item">
          <img src="@/assets/images/chinchorro-wayuu.jpg" alt="Chinchorro Wayúu" />
          <h3>Chinchorro</h3>
          <p>El chinchorro es una hamaca tejida, fundamental en la vida cotidiana Wayúu, símbolo de descanso, familia y hospitalidad.</p>
          <a href="https://artesaniasdecolombia.com.co/PortalAC/C_ferias/chinchorros-mochilas-y-encierro-historia-de-las-wayu_10194" target="_blank" class="more-info">Conoce más aquí</a>
        </div>
      </div>
    </section>
    <div class="simbolos-main-content">
      <div class="simbolos-main">
        <section class="castas-section">
          <h2>Castas y Grupos (Eiruku) Wayúu</h2>
          <div class="castas-grid">
            <div class="casta-item">
              <img src="@/assets/images/pushaina.jpeg" alt="Casta Puushaina" />
              <h3>Puushaina</h3>
              <p>Una de las castas más reconocidas, con gran influencia en la cultura y la historia Wayúu.</p>
            </div>
            <div class="casta-item">
              <img src="@/assets/images/ipuana.jpeg" alt="Casta Epushii" />
              <h3>Ipuana</h3>
              <p>Grupo destacado por su liderazgo y sabiduría en la toma de decisiones comunitarias.</p>
            </div>
            <div class="casta-item">
              <img src="@/assets/images/epinayu.jpeg" alt="Casta Uraliyuu" />
              <h3>Epinayu</h3>
              <p>Tribu con fuerte arraigo en la tradición oral y la protección de los valores Wayúu.</p>
            </div>
          </div>
          <div class="castas-info">
            <p>Las castas Wayúu, conocidas como "eiruku", son grupos familiares que definen la identidad, el linaje y la pertenencia dentro de la sociedad. Cada casta tiene símbolos, colores y relatos propios que se transmiten de generación en generación.</p>
          </div>
        </section>
        <section class="videos-section">
          <h2>Videos para conocer más sobre la cultura Wayúu</h2>
          <div class="videos-grid">
            <div class="video-item">
              <YoutubeLazy videoId="QaLYTVOmzwA" title="Cultura Wayúu" />
              <p>Documental: Cultura y tradiciones Wayúu</p>
            </div>
            <div class="video-item">
              <YoutubeLazy videoId="KqbmYP1bwMU" title="Símbolos Wayúu" />
              <p>Significado de los símbolos y colores Wayúu</p>
            </div>
          </div>
        </section>
      </div>
      <aside class="simbolos-sidebar">
        <section class="castas-more">
          <h2>Más sobre las Castas</h2>
          <img src="@/assets/images/wayuu-bg.jpg" alt="Simbolos de todas las castas Wayúu" class="castas-bg" />
          <p>Existen más simbolos y castas de la etnia, para conocer más acerca de ellas <a href="https://es.scribd.com/doc/58422145/Los-WayuU-Y-Sus-Castas" target="_blank" class="more-info">Visita Aquí</a></p>
        </section>
        <section class="info-extra">
          <h2>¿Sabías qué?</h2>
          <ul>
            <li>La sociedad Wayúu es matrilineal: la herencia y el linaje se transmiten por la madre.</li><br>
            <li>El idioma Wayuunaiki es fundamental para la transmisión de la cultura y la identidad.</li><br>
            <li>Las celebraciones y rituales Wayúu están llenos de simbolismo y respeto por la naturaleza.</li>
          </ul>
        </section>
      </aside>
    </div>
  </div>
  <FooterComponent />
</template>

<script setup>
import HeaderPublic from '@/components/HeaderPublic.vue';
import FooterComponent from '@/components/FooterComponent.vue';
import YoutubeLazy from '@/components/YoutubeLazy.vue';
</script>

<style scoped>
.simbolos-view {
  min-height: 100vh;
  background: var(--light-bg);
  display: flex;
  flex-direction: column;
}
.simbolos-header {
  background-image: linear-gradient(rgba(215,38,56,0.85), rgba(215,38,56,0.85)), url('@/assets/images/fondo-header.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 60px 0 40px 0;
  text-align: center;
}
.simbolos-header h1 {
  color: #fff;
  font-size: 2.5rem;
  font-weight: bold;
  letter-spacing: 2px;
  margin: 0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.18);
}
.simbolos-section {
  max-width: 1100px;
  margin: 40px auto 0 auto;
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2rem 1.5rem;
  margin-bottom: 40px;
}
.simbolos-section h2 {
  color: var(--primary-color);
  margin-bottom: 1.2rem;
}
.simbolos-grid {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 1.5rem;
}
.simbolo-item {
  background: var(--light-bg);
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
  padding: 1rem;
  text-align: center;
  width: 270px;
  max-width: 95vw;
}
.simbolo-item img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 0.7rem;
  border: 3px solid var(--accent-color);
}
.simbolo-item h3 {
  color: var(--accent-color);
  margin-bottom: 0.4rem;
  font-size: 1.1rem;
}
.simbolo-item p {
  color: var(--text-color);
  font-size: 0.98rem;
}
.simbolo-item:hover{
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(27,27,30,0.12);
}
.more-info:hover {
  color: var(--primary-color);
  text-decoration: underline;
}

.simbolos-main-content {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto 40px auto;
  width: 100%;
  align-items: flex-start;
}
.simbolos-main {
  flex: 2;
  min-width: 0;
}
.simbolos-sidebar {
  flex: 1;
  min-width: 270px;
  max-width: 350px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.simbolos-sidebar h2{
    color: #FFBA08;;
}
.castas-section, .videos-section {
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2rem 1.5rem;
  margin-bottom: 2rem;
}
.castas-section h2, .videos-section h2 {
  color: var(--primary-color);
  margin-bottom: 1.2rem;
}
.castas-grid, .videos-grid {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 1.5rem;
}
.casta-item, .video-item {
  background: var(--light-bg);
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
  padding: 1rem;
  text-align: center;
  width: 270px;
  max-width: 95vw;
}
.videos-section{
    width: 1000px;
    margin: 40px auto 0 80px;
}
.casta-item img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 0.7rem;
  border: 3px solid var(--accent-color);
}
.casta-item h3 {
  color: var(--accent-color);
  margin-bottom: 0.4rem;
  font-size: 1.1rem;
}
.casta-item p {
  color: var(--text-color);
  font-size: 0.98rem;
}
.casta-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(27,27,30,0.12);
}
.castas-info {
  margin-top: 1.2rem;
  color: var(--text-color);
  font-size: 1.05rem;
  text-align: center;
}
.video-item p {
  margin-top: 0.7rem;
  color: var(--primary-color);
  font-size: 1rem;
}
.castas-more {
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
  padding: 1.2rem 1rem;
  margin-bottom: 1.2rem;
}
.castas-more .castas-bg {
  width: 80%;
  max-width: 180px;
  display: block;
  margin: 0 auto 0.7rem auto;
  border-radius: 0.7rem;
  object-fit: cover;
}
.info-extra {
  background: #fff8e1;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
  padding: 1.2rem 1rem;
  margin-bottom: 1.2rem;
}
.info-extra ul {
  margin: 0;
  color: var(--accent-color);
  font-size: 1.08rem;
  list-style: disc inside;
}
.info-extra ul li:hover {
  color: var(--primary-color);
  
}
@media (max-width: 1100px) {
  .simbolos-main-content {
    flex-direction: column;
    gap: 1.5rem;
    max-width: 100vw;
  }
  .simbolos-sidebar {
    max-width: 100vw;
    min-width: 0;
    flex-direction: column;
    gap: 1.5rem;
  }
  .castas-more .castas-bg {
    width: 100%;
    max-width: 100vw;
  }
}
@media (max-width: 900px) {
  .simbolos-section, .castas-section, .videos-section {
    padding: 1.2rem 0.7rem;
  }
  .simbolos-header {
    padding: 40px 0 24px 0;
  }
  .simbolos-header h1 {
    font-size: 2rem;
  }
  .simbolos-grid, .castas-grid, .videos-grid {
    flex-direction: column;
    gap: 1.2rem;
    align-items: center;
  }
  .simbolo-item, .casta-item, .video-item {
    width: 100%;
    max-width: 100vw;
  }
}
</style>
