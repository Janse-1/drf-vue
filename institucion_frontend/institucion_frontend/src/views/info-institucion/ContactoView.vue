<template>
  <HeaderPublic />
  <div class="about">
    <h1 class="titulo-sedes">Contáctate con una de nuestras sedes</h1>
    <p><strong>Para más información, puedes contactarnos a través de los siguientes medios:</strong></p>
  </div>
  <div class="sedes-container">
    <div v-for="sede in sedes" :key="sede.nombre" class="sede-card">
      <h2 class="sede-nombre">{{ sede.nombre }}</h2>
      <p class="sede-direccion"><i class="fa-solid fa-location-dot"></i> {{ sede.direccion }}</p>
      <p class="sede-correo">
        <i class="fa-solid fa-envelope"></i>
        <a :href="`mailto:${sede.correo}`" class="correo-link">{{ sede.correo }}</a>
        <button class="icono-correo" :title="`Enviar correo a ${sede.nombre}`" @click="enviarCorreo(sede.correo)">
          <i class="fa-solid fa-paper-plane"></i>
        </button>
      </p>
      <p class="sede-contacto"><i class="fa-solid fa-phone"></i> {{ sede.contacto }}</p>
      <p class="sede-descripcion">{{ sede.descripcion }}</p>
    </div>
  </div>
  <FooterComponent />
</template>

<script setup>
import HeaderPublic from '@/components/HeaderPublic.vue'
import FooterComponent from '@/components/FooterComponent.vue'
import { ref } from 'vue'

const sedes = ref([
  {
    nombre: 'Sede Principal LIMONCITO',
    direccion: 'Calle 1 #23-45, Maicao',
    correo: 'limoncito@iei1.edu.co',
    contacto: '+57 300 111 1111',
    descripcion: 'La sede principal cuenta con primaria y secundaria, brindando atención integral a la comunidad.',
  },
  {
    nombre: 'Sede PIYUSHIPANA',
    direccion: 'Carrera 2 #34-56, Maicao',
    correo: 'piyushipana@iei1.edu.co',
    contacto: '+57 300 222 2222',
    descripcion: 'Ubicada en el barrio San José, esta sede ofrece educación básica y media con enfoque intercultural.',
  },
  {
    nombre: 'Sede MARIA CONCEPCIÓN EPINAYU',
    direccion: 'Transversal 3 #45-67, Maicao',
    correo: 'cepinayu@iei1.edu.co',
    contacto: '+57 300 333 3333',
    descripcion: 'Sede con espacios verdes y aulas especializadas para el desarrollo de actividades lúdicas y deportivas.',
  },
  {
    nombre: 'Sede NARANJITO 1',
    direccion: 'Calle 4 #56-78, Maicao',
    correo: 'naranjito1@iei1.edu.co',
    contacto: '+57 300 444 4444',
    descripcion: 'Reconocida por su ambiente inclusivo y programas de apoyo escolar para estudiantes.',
  },
  {
    nombre: 'Sede NARANJITO 2',
    direccion: 'Carrera 5 #67-89, Maicao',
    correo: 'naranjito2@iei1.edu.co',
    contacto: '+57 300 555 5555',
    descripcion: 'Enfocada en la innovación educativa y el uso de tecnología en el aula.',
  },
  {
    nombre: 'Sede JONJONCITO',
    direccion: 'Calle 6 #78-90, Maicao',
    correo: 'jonjoncito@iei1.edu.co',
    contacto: '+57 300 666 6666',
    descripcion: 'Sede con programas de integración para comunidades indígenas y rurales.',
  },
  {
    nombre: 'Sede LANTASIRA',
    direccion: 'Carrera 7 #89-01, Maicao',
    correo: 'lantasira@iei1.edu.co',
    contacto: '+57 300 777 7777',
    descripcion: 'Destacada por su oferta de actividades extracurriculares y deportivas.',
  },
  {
    nombre: 'Sede SACHIKIMA>ANA',
    direccion: 'Calle 8 #90-12, Maicao',
    correo: 'sachikima@iei1.edu.co',
    contacto: '+57 300 888 8888',
    descripcion: 'Cuenta con laboratorios de ciencias y tecnología para todos los grados.',
  },
  {
    nombre: 'Sede MULAMA>ANA',
    direccion: 'Carrera 9 #12-34, Maicao',
    correo: 'mulama@iei1.edu.co',
    contacto: '+57 300 999 9999',
    descripcion: 'Sede con enfoque en valores y formación ciudadana.',
  },
  {
    nombre: 'Sede LA VOLUNTAD DE DIOS',
    direccion: 'Calle 10 #23-45, Maicao',
    correo: 'lavDios@iei1.edu.co',
    contacto: '+57 300 101 0101',
    descripcion: 'Promueve la convivencia y el respeto a la diversidad cultural.',
  },
  {
    nombre: 'Sede MAIMAJASAY',
    direccion: 'Carrera 11 #34-56, Maicao',
    correo: 'maimajasay@iei1.edu.co',
    contacto: '+57 300 202 0202',
    descripcion: 'Sede rural con proyectos de agricultura escolar y sostenibilidad.',
  },
])

function enviarCorreo(correo) {
  window.location.href = `mailto:${correo}`
}
</script>

<style scoped>
.about {
  text-align: center;
  padding: 2rem;
  background: var(--light-bg);
  justify-content: center;
}
.about p {
  font-size: 0.9rem;
  color: #000;
  height: 30px;
  background-color: #fdf1c4;
  padding: 10px;
  border-left: 4px solid #FFBA08;
  margin-bottom: 1rem;
  border-radius: 6px;
}
.about p:hover {
  background-color: #fcebbd;
  cursor: pointer;
  transition: background-color 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

}
.titulo-sedes {
  color: var(--primary-color);
  font-size: 2rem;
  margin-bottom: 1rem;
}
.titulo-sedes::after {
  content: '';
  display: block;
  width: 500px;
  height: 4px;
  background-color: var(--accent-color);
  margin: 0.5rem auto;
}
.titulo-sedes:hover {
  color: #FFBA08;
  transition: color 0.3s ease;
}
.sedes-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
  padding: 2rem 1rem 4rem 1rem;
  background: var(--light-bg);
}
.sede-card {
  background: white;
  border: 2px solid var(--primary-color);
  border-radius: 1.2rem;
  box-shadow: 0 4px 16px rgba(27,27,30,0.08);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  width: 320px;
  max-width: 95vw;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: box-shadow 0.2s;
  margin-bottom: 1rem;
}
.sede-card:hover {
  box-shadow: 0 8px 32px rgb(255, 193, 7);
  border-color: var(--accent-color);
}
.sede-nombre {
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-size: 1.4rem;
  font-weight: bold;
}
.sede-direccion, .sede-correo, .sede-contacto {
  margin: 0.2rem 0;
  color: var(--accent-color);
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.sede-descripcion {
  margin-top: 0.7rem;
  color: var(--text-color);
  font-size: 0.98rem;
}
.icono-correo {
  background: var(--secondary-color);
  border: none;
  border-radius: 50%;
  padding: 0.3rem 0.5rem;
  margin-left: 0.5rem;
  cursor: pointer;
  color: var(--primary-color);
  font-size: 1.1rem;
  transition: background 0.2s;
}
.icono-correo:hover {
  background: var(--primary-color);
  color: white;
}
.correo-link {
  color: var(--accent-color);
  text-decoration: underline;
}
@media (max-width: 900px) {
  .sedes-container {
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }
  .sede-card {
    width: 98vw;
    max-width: 98vw;
  }
}
</style>
