<template>
  <div class="youtube-lazy" @click="loadVideo">
    <img
      :src="thumbnail"
      :alt="title"
      loading="lazy"
    />
    <div class="play-button"></div>
    <iframe
      v-if="isVideoLoaded"
      :src="embedUrl"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
    ></iframe>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  videoId: String,
  title: String
})

const isVideoLoaded = ref(false)

const thumbnail = computed(() =>
  `https://img.youtube.com/vi/${props.videoId}/hqdefault.jpg`
)

const embedUrl = computed(() =>
  `https://www.youtube.com/embed/${props.videoId}?autoplay=1`
)

const loadVideo = () => {
  isVideoLoaded.value = true
}
</script>

<style scoped>
.youtube-lazy {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 ratio */
  background: #000;
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
}
.youtube-lazy img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  top: 0;
  left: 0;
  transition: filter 0.3s;
}
.youtube-lazy:hover img {
  filter: brightness(0.8);
}
.youtube-lazy iframe {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  border: none;
}
.play-button {
  position: absolute;
  width: 64px;
  height: 64px;
  background: url('https://img.icons8.com/ios-filled/100/ffffff/play-button-circled.png') no-repeat center;
  background-size: contain;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.8;
}
</style>
