<template>
    <HeaderPublic />
  <div class="quienes-somos-view">
        <div class="header-bg-etnia">
            <h1>¿Quiénes somos?</h1>
        </div>
        <section class="intro-wayuu">
         <div class="intro-content">
            <div class="intro-main">
            <h2>La Etnia Wayúu</h2>
            <div class="wayuu-carousel">
                <img v-for="(img, idx) in wayuuImages" :key="idx" :src="img" alt="Etnia Wayúu" class="carousel-img" />
            </div>
            <p>
                La etnia Wayúu, originaria de la península de La Guajira, es reconocida por su riqueza cultural, su lengua propia y sus tradiciones ancestrales. Su cosmovisión, respeto por la naturaleza y sentido de comunidad han sido pilares fundamentales en la región, inspirando a generaciones a mantener vivas sus raíces.
            </p>
            </div>
            <div class="escudo-box">
            <img src="@/assets/images/logo.png" alt="Escudo del Colegio" class="escudo-img" />
            <div class="escudo-desc">
                <h3>Escudo Institucional</h3>
                <p>
                El escudo de la Institución Educativa Indígena N°1 representa la unión entre el conocimiento ancestral Wayúu y la educación moderna. Sus colores y símbolos reflejan la identidad, la sabiduría, la protección de la cultura y el compromiso con el futuro de la comunidad.
                </p>
            </div>
            </div>
        </div>
     </section>
    <section class="historia-deseo-container">
      <div class="historia-institucion">
        <h2>Nuestra Historia</h2>
        <div class="historia-carousel">
          <img v-for="(img, idx) in historiaImages" :key="idx" :src="img" alt="Historia Institución" class="carousel-img" />
        </div>
        <p>
          La Institución Educativa Indígena N°1 nació del sueño colectivo de líderes Wayúu y educadores comprometidos con el desarrollo de su pueblo. Desde sus inicios, la institución ha buscado ser un puente entre el conocimiento ancestral y la educación moderna, promoviendo el respeto, la identidad y la excelencia académica.<br><br>
          A lo largo de los años, hemos crecido junto a la comunidad, adaptándonos a los cambios y desafíos, pero siempre manteniendo la esencia de nuestra misión y visión. <a href="#mision-vision" class="enlace-mision">Conoce nuestra misión y visión</a> para descubrir los valores que nos guían.
        </p>
      </div>
      <div class="historia-lateral">
        <section class="deseo-futuro">
          <p>
            Nuestro mayor deseo es seguir construyendo nuevos sueños, abriendo caminos de esperanza y oportunidades para más personas y jóvenes Wayúu, fortaleciendo así el tejido social y cultural de nuestra región.
          </p>
        </section>
        <section class="frase-garzon">
          <blockquote>
            "Si ustedes los jóvenes no asumen la dirección de su propio país, nadie va a venir a salvárselo. ¡Nadie!"
          </blockquote>
          <span class="autor">- Jaime Garzón</span>
        </section>
      </div>
    </section>
  </div>

  <FooterComponent />
</template>

<script setup>
import FooterComponent from '@/components/FooterComponent.vue';
import HeaderPublic from '@/components/HeaderPublic.vue';
import wayuu1 from '@/assets/images/Wayuu.jpg'
import wayuu2 from '@/assets/images/images.jpg'
import historia1 from '@/assets/images/Wayuuu.jpeg'
import historia2 from '@/assets/images/images (1).jpg'

const wayuuImages = [wayuu1, wayuu2]
const historiaImages = [historia1, historia2]
</script>

<style scoped>
.quienes-somos-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--light-bg);
  margin-bottom: 60px;
}

.header-bg-etnia {
  background-image: linear-gradient(rgba(215,38,56,0.7), rgba(215,38,56,0.7)), url('@/assets/images/foto-wayuu.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 60px 0 40px 0;
  text-align: center;
}

.header-bg-etnia h1 {
  color: #fff;
  font-size: 3.5rem;
  font-weight: bold;
  letter-spacing: 2px;
  margin: 0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.18);
  animation: colorGrow 2.5s infinite alternate;
}

@keyframes colorGrow {
  0% { color: #ffc107; transform: scale(0.8); text-shadow: 0 2px 8px rgba(0,0,0,0.18); }
  25% { color: #fada24; transform: scale(1.0); text-shadow: 0 4px 12px rgba(215,38,56,0.18); }
  50% { color: #d72638; transform: scale(1.0); text-shadow: 0 6px 16px rgba(250,218,36,0.18); }
  75% { color: #fada24; transform: scale(1.0); text-shadow: 0 4px 12px rgba(215,38,56,0.18); }
  100% { color: #ffc107; transform: scale(0.8); text-shadow: 0 2px 8px rgba(0,0,0,0.18); }
}

/* Sección Intro Wayuu */
.intro-wayuu,
.historia-deseo-container {
  max-width: 1100px;
  margin: 40px auto 0 auto;
}

.intro-wayuu {
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2rem 1.5rem;
}

.intro-content {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
  align-items: flex-start;
}

.intro-main { flex: 2; }

.escudo-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f8f8;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(27,27,30,0.08);
  padding: 1.2rem 1rem;
  min-width: 220px;
  max-width: 270px;
  transition: box-shadow 0.3s, transform 0.3s;
}
.escudo-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(27,27,30,0.12);
}
.escudo-img {
  width: 100px;
  height: auto;
  margin-bottom: 0.7rem;
}
.escudo-desc { text-align: center; }
.escudo-desc h3 {
  color: var(--primary-color);
  margin-bottom: 0.3rem;
  font-size: 1.1rem;
}
.escudo-desc p {
  color: var(--text-color);
  font-size: 0.98rem;
}

/* Carruseles */
.wayuu-carousel, .historia-carousel {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1.2rem;
  padding-bottom: 0.5rem;
  overflow: hidden;
  position: relative;
  width: 100%;
}
.carousel-img {
  height: 140px;
  border-radius: 10px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(27,27,30,0.10);
  background: #eee;
  transition: transform 0.3s cubic-bezier(.4,2,.6,1), filter 0.3s;
  will-change: transform, filter;
  max-width: 400px;
  max-height: 140px;
  min-width: 0;
  min-height: 0;
}
.wayuu-carousel .carousel-img:hover,
.historia-carousel .carousel-img:hover {
  transform: scale(1.25);
  z-index: 2;
  filter: brightness(1.1);
}
.wayuu-carousel:hover .carousel-img:not(:hover),
.historia-carousel:hover .carousel-img:not(:hover) {
  transform: scale(0.85);
  filter: brightness(0.85) blur(1px);
  z-index: 1;
}

/* Historia y lateral */
.historia-deseo-container {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
  align-items: flex-start;
}
.historia-institucion {
  flex: 2;
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2rem 1.5rem;
  max-width: 100%;
  transition: box-shadow 0.3s, transform 0.3s;
}
.historia-institucion:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(27,27,30,0.12);
}
.historia-institucion h2 {
  color: var(--accent-color);
  margin-bottom: 0.7rem;
}
.historia-institucion p {
  color: var(--text-color);
  font-size: 1.1rem;
}

.historia-lateral {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 270px;
  max-width: 350px;
}

/* Deseo futuro y frase Garzón */
.deseo-futuro, .frase-garzon {
  max-width: 100%;
  margin: 0;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 1.5rem 1.2rem;
  text-align: center;
  transition: box-shadow 0.3s, transform 0.3s;
}
.deseo-futuro {
  background: var(--accent-color);
  color: #fff;
  font-size: 1.15rem;
}
.deseo-futuro:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgb(245, 22, 22);
}
.frase-garzon {
  background: #fff;
  font-style: italic;
  color: var(--primary-color);
}
.frase-garzon:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgb(237, 252, 31);
}
.frase-garzon blockquote {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 500;
}
.frase-garzon .autor {
  display: block;
  color: var(--accent-color);
  font-size: 1rem;
  margin-top: 0.5rem;
}

/* Títulos y enlaces */
.intro-wayuu h2 {
  color: var(--primary-color);
  margin-bottom: 0.7rem;
}
.intro-wayuu p {
  color: var(--text-color);
  font-size: 1.1rem;
}
.enlace-mision {
  color: var(--primary-color);
  text-decoration: underline;
  cursor: pointer;
}
.enlace-mision:hover {
  color: #fada24;
}

/* Responsive */
@media (max-width: 1100px) {
  .intro-content,
  .historia-deseo-container {
    flex-direction: column;
    gap: 1.5rem;
    max-width: 100%;
  }
  .escudo-box,
  .historia-lateral {
    max-width: 100%;
    min-width: 0;
    margin: 0 auto;
    flex-direction: column;
    gap: 1.5rem;
  }
  .deseo-futuro, .frase-garzon {
    margin: 40px auto 32px auto;
  }
}
@media (max-width: 900px) {
  .intro-wayuu, .historia-institucion, .deseo-futuro {
    padding: 1.2rem 0.7rem;
  }
  .header-bg-etnia {
    padding: 40px 0 24px 0;
  }
  .header-bg-etnia h1 {
    font-size: 2rem;
  }
  .carousel-img,
  .wayuu-carousel .carousel-img,
  .historia-carousel .carousel-img {
    height: 90px;
    max-width: 120px;
    max-height: 90px;
    flex: 0 0 120px;
  }
}
</style>
