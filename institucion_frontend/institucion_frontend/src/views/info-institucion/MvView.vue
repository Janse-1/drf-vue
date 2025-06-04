<template>
  <HeaderPublic />
  <div class="mv-view">
    <div class="mv-header">
      <h1>Misión y Visión</h1>
    </div>
    <section class="mv-section mv-mision">
      <h2>Misión</h2>
      <p>
        La Institución Educativa Indígena N°1 de La Guajira, con sus 11 sedes y más de 3.000 estudiantes, tiene como misión formar ciudadanos íntegros,
        críticos y comprometidos con el desarrollo de su comunidad y la preservación de la cultura Wayúu. Promovemos una educación intercultural de
        calidad, basada en valores, el respeto por la diversidad y el fortalecimiento de la identidad étnica, integrando el conocimiento ancestral 
        con los avances de la educación moderna.
      </p>
    </section>
    <section class="mv-section mv-vision">
      <h2>Visión</h2>
      <p>
        En el año 2030, la Institución Educativa Indígena N°1 será reconocida
        como un referente regional y nacional en educación intercultural, inclusiva
        e innovadora. Aspiramos a que nuestros egresados sean líderes
        transformadores, orgullosos de sus raíces, capaces de construir un futuro
        sostenible y de contribuir al bienestar de la sociedad, manteniendo vivas
        las tradiciones y valores de la etnia Wayúu.
      </p>
    </section>
  </div>
  <FooterComponent />
</template>

<script setup>
import HeaderPublic from '@/components/HeaderPublic.vue';
import FooterComponent from '@/components/FooterComponent.vue';
</script>

<style scoped>
.mv-view {
  min-height: 100vh;
  background: var(--light-bg);
  display: flex;
  flex-direction: column;
  margin-bottom: 60px;
}
.mv-header {
  background-image: linear-gradient(rgba(215, 38, 38, 0.85), rgba(63, 59, 59, 0.85)), url('@/assets/images/footer_bg.png');
  background-size: cover;
  background-position: below center;
  background-repeat: no-repeat;
  padding: 60px 0 40px 0;
  text-align: center;
}
.mv-header h1 {
  color: #fff;
  font-size: 2.7rem;
  font-weight: bold;
  letter-spacing: 2px;
  margin: 0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.18);
  font-family: 'Segoe UI', sans-serif;
}
.mv-section {
  max-width: 900px;
  margin: 40px auto 0 auto;
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2.5rem 2rem;
  font-family: 'Segoe UI', sans-serif;
}
.mv-section h2 {
  color: var(--primary-color);
  font-size: 1.7rem;
  margin-bottom: 1rem;
  font-weight: bold;
}
.mv-section p {
  color: var(--text-color);
  font-size: 1.15rem;
  line-height: 1.7;
}
.mv-vision h2 {
  color: var(--accent-color);
}
@media (max-width: 900px) {
  .mv-section {
    padding: 1.2rem 0.7rem;
  }
  .mv-header {
    padding: 40px 0 24px 0;
  }
  .mv-header h1 {
    font-size: 2rem;
  }
}
</style>
