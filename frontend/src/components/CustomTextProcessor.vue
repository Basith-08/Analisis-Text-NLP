<template>
  <div>
    <h3>Proses Teks Custom</h3>

    <div class="mb-2">
      <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">
        Masukkan Teks:
      </label>
      <textarea
        v-model="customText"
        rows="6"
        placeholder="Masukkan teks yang ingin diproses..."
        style="resize: vertical;"
      ></textarea>
    </div>

    <button
      @click="processText"
      :disabled="!customText.trim() || loading"
      style="width: 100%;"
    >
      <span v-if="loading" class="loading"></span>
      <span v-else>Proses Teks</span>
    </button>

    <!-- Example texts -->
    <div class="mt-2" style="padding: 1rem; background: var(--bg-color); border-radius: 8px;">
      <p style="font-weight: 500; margin-bottom: 0.5rem;">Contoh Teks:</p>
      <button
        class="secondary"
        style="width: 100%; margin-bottom: 0.5rem; text-align: left;"
        @click="customText = 'Semoga tahun ini lulus UI aamiin 🤲 love it! ❤️'"
      >
        Contoh 1: Teks dengan emoji
      </button>
      <button
        class="secondary"
        style="width: 100%; margin-bottom: 0.5rem; text-align: left;"
        @click="customText = 'UI emang the best campus! Keren banget sih videonya 😍🔥'"
      >
        Contoh 2: Teks campuran Indonesia-Inggris
      </button>
      <button
        class="secondary"
        style="width: 100%; text-align: left;"
        @click="customText = 'Follow @ui_official di TikTok! Info lengkap di https://ui.ac.id #UniversitasIndonesia'"
      >
        Contoh 3: Teks dengan URL dan hashtag
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'CustomTextProcessor',
  props: {
    loading: Boolean
  },
  emits: ['process'],
  setup(props, { emit }) {
    const customText = ref('')

    const processText = () => {
      emit('process', customText.value)
    }

    return {
      customText,
      processText
    }
  }
}
</script>
