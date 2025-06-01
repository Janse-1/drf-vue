<template>
  <div class="home-container">
    <HeaderPublic />

    <main class="main-content">
      <section class="hero">
        <div class="hero-text">
          <h1>Bienvenido al Sistema Académico</h1>
          <p>Una plataforma para facilitar la gestión de notas, boletines y el seguimiento académico de los estudiantes Wayuu.</p>
        </div>
      </section>

      <section class="info">
        <h2>¿Quiénes somos?</h2>
        <p>
          Somos la Institución Educativa Indígena N°1 de La Guajira. Nuestra misión es promover una educación con identidad,
          fortaleciendo la cultura Wayuu mediante el uso de tecnologías modernas.
        </p>

        <h2>¿Qué es este sistema?</h2>
        <p>
          Es una plataforma desarrollada para permitir a los docentes, padres y coordinadores acceder fácilmente a la información
          académica de los estudiantes.
        </p>
      </section>
    </main>

    <FooterComponent />
  </div>
</template>

<script setup>
import FooterComponent from '@/components/FooterComponent.vue';
import HeaderPublic from '@/components/HeaderPublic.vue';

</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* Fondo con imagen sutil y superposición */
  background: 
    linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
    url('../assets/images/fondooo.png') center/cover no-repeat;
}

.main-content {
  flex: 1;
  padding: 20px;
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: var(--light-bg);
  padding: 30px 10px;
  text-align: center;
}

.hero-image {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  margin-bottom: 20px;
}

.hero-text h1 {
  font-size: 2em;
  color: var(--primary-color);
}

.hero-text p {
  font-size: 1.2em;
  max-width: 700px;
}

.info {
  margin-top: 40px;
}

.info h2 {
  color: var(--accent-color);
  margin-top: 20px;
}
</style>
