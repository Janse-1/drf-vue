<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section logo-section">
        <img src="@/assets/images/logo.png" alt="Logo IEI" class="logo" />
        <p>Institución Educativa Indígena N°1</p>
        <p>Maicao, La Guajira - Colombia</p>
        <p>NIT: 892115029-4</p>
      </div>

      <div class="footer-section contacto-section">
        <h4>Contáctanos</h4>
        <p>Email: contacto@iei1.edu.co</p>
        <p>Teléfono: +57 300 000 0000</p>
        <p>Horario: Lun a Vie - 8 AM a 12 PM / 2 PM a 6 PM</p>
      </div>

      <div class="footer-section sitio-section">
        <h4>Acerca del sitio</h4>
        <ul>
          <li><a href="#">Términos y condiciones</a></li>
          <li><a href="#">Política de privacidad</a></li>
          <li><a href="#">Ayuda</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <img src="../assets/images/footer_bg.png" alt="Decoración Wayuu" class="footer-bg" />
      <p>© 2025 IEI N°1. Todos los derechos reservados. Desarrollado por el equipo de Ingeniería de Sistemas.</p>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped>
.footer {
  background-color: #1B1B1E;
  color: #f1f1f1;
  font-family: 'Segoe UI', sans-serif;
  padding-top: 2rem;
  border-top: 5px solid #D72638;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  text-align: left;
  padding: 0 2rem 2rem;
}

.footer-section {
  flex: 1;
  min-width: 200px;
  margin-bottom: 1.5rem;
}

.footer-section h4 {
  color: #FFBA08;
  margin-bottom: 1rem;
}

.logo {
  width: 80px;
  margin-bottom: 1rem;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  color: #f1f1f1;
  text-decoration: none;
}

.footer-section a:hover {
  color: #FFBA08;
}

.footer-bottom {
  text-align: center;
  position: relative;
  padding-top: 1rem;
  border-top: 1px solid #444;
  font-size: 0.9rem;
}

.footer-bg {
  width: 100%;
  margin-top: 1rem;
  opacity: 0.1;
  position: absolute;
  top: -60px;
  left: 0;
  z-index: 0;
}
</style>
