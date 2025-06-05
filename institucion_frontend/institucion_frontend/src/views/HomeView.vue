<template>
  <div class="home-container">
    <div v-show="showVideo" class="video-bg">
      <video src="../assets/images/fondo-ie.mp4" class="video-bg-video" autoplay loop muted playsinline></video>
      <div class="video-overlay">
        <div class="video-center-content">
          <h1>Bienvenido! a la Institución Educativa Indigena N1</h1>
        </div>
        <div class="scroll-down-indicator">
          <i class="fa-solid fa-chevron-down"></i>
        </div>
      </div>
    </div>
    <HeaderPublic class="header-solid" />
    <main class="main-content">
      <section class="destacados" id="destacados">
        <h2>¿Por qué elegirnos?</h2>
        <div class="features-grid">
          <div class="feature-item">
            <i class="fa-solid fa-laptop-code"></i>
            <h3>Plataforma Digital</h3>
            <p>Acceso rápido y seguro a notas, boletines y reportes desde cualquier dispositivo.</p>
          </div>
          <div class="feature-item">
            <i class="fa-solid fa-people-group"></i>
            <h3>Comunidad Intercultural</h3>
            <p>Fomentamos el respeto, la diversidad y la identidad Wayúu en cada espacio educativo.</p>
          </div>
          <div class="feature-item">
            <i class="fa-solid fa-award"></i>
            <h3>Excelencia Académica</h3>
            <p>Docentes capacitados y programas innovadores para el desarrollo integral de los estudiantes.</p>
          </div>
        </div>
      </section>
    </main>
    <FooterComponent class="footer-solid" />
  </div>
</template>

<script setup>
import FooterComponent from '@/components/FooterComponent.vue';
import HeaderPublic from '@/components/HeaderPublic.vue';
import { ref, onMounted, onBeforeUnmount } from 'vue';

const showVideo = ref(true);

const handleScroll = () => {
  showVideo.value = window.scrollY < window.innerHeight * 0.5;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  // Scroll suave al hacer clic en el indicador
  const indicator = document.querySelector('.scroll-down-indicator');
  if (indicator) {
    indicator.addEventListener('click', () => {
      const destacados = document.getElementById('destacados');
      if (destacados) {
        destacados.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }
});
onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.home-container {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.video-bg {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  overflow: hidden;
}
.video-bg-video {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  filter: brightness(0.7) blur(1px);
  pointer-events: none;
  user-select: none;
}
.video-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  width: 100vw;
  height: 100vh;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
}
.header-solid {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
}
.footer-solid {
  position: relative;
  width: 100%;
  
}
.video-center-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.video-center-content h1 {
  color: #fff;
  font-size: 2.5rem;
  font-weight: bold;
  text-align: center;
  margin: 0;
  padding: 0 20px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.18);
  overflow: hidden;
  white-space: nowrap;
  border-right: 3px solid #fff;
  width: 0;
  animation: typing 3s steps(40, end) 0.3s 1 normal both, blink-cursor 0.7s steps(1) infinite;
}

@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}

@keyframes blink-cursor {
  0%, 100% { border-right-color: #fff; }
  50% { border-right-color: transparent; }
}
.scroll-down-indicator {
  position: absolute;
  left: 50%;
  bottom: 40px;
  transform: translateX(-50%);
  z-index: 4;
  font-size: 2.5rem;
  color: var(--accent-color);
  cursor: pointer;
  animation: bounce 1.5s infinite;
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  padding: 0.5rem 0.7rem;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
}
@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(18px); }
}
.main-content {
  position: relative;
  z-index: 5;
  flex: 1;
  padding: 0 0 40px 0;
  margin-top: 100vh;
  min-height: 100vh;
  /* Asegura espacio para el footer */
  margin-bottom: 120px;
}
.destacados {
  margin: 60px auto 0 auto;
  max-width: 1100px;
  background: #fff;
  border-radius: 1.2rem;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2.5rem 2rem;
  text-align: center;
}
.destacados h2 {
  color: var(--accent-color);
  margin-bottom: 2rem;
}
.features-grid {
  display: flex;
  gap: 2.5rem;
  justify-content: center;
  flex-wrap: wrap;
}
.feature-item {
  flex: 1 1 220px;
  min-width: 220px;
  max-width: 320px;
  background: var(--light-bg);
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
  padding: 1.5rem 1rem;
  margin-bottom: 1.2rem;
  text-align: center;
}
.feature-item i {
  font-size: 2.2rem;
  color: var(--primary-color);
  margin-bottom: 0.7rem;
}
.feature-item h3 {
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-size: 1.15rem;
}
.feature-item p {
  color: var(--text-color);
  font-size: 1rem;
}
@media (max-width: 900px) {
  .main-content {
    padding: 0 0 20px 0;
  }
  .destacados, .testimonios {
    padding: 1.2rem 0.7rem;
  }
  .features-grid, .testimonios-grid {
    flex-direction: column;
    gap: 1.2rem;
    align-items: center;
  }
  .feature-item, .testimonio-item {
    width: 100%;
    max-width: 100vw;
  }
}
</style>
