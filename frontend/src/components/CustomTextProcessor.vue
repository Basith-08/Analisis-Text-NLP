<template>
  <div>
    <h3>Prediksi Sentimen Teks</h3>

    <div class="mb-2">
      <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">
        Masukkan Teks:
      </label>
      <textarea
        v-model="customText"
        rows="6"
        placeholder="Masukkan teks yang ingin diprediksi sentimennya..."
        style="resize: vertical;"
      ></textarea>
    </div>
    
    <div class="form-group">
      <input type="checkbox" id="apply_stemming_pred" v-model="applyStemming" />
      <label for="apply_stemming_pred" style="margin-left: 8px;">Gunakan Stemming saat Prediksi</label>
    </div>

    <div class="button-group">
      <button
        @click="handlePredict"
        :disabled="!customText.trim() || loading"
      >
        <span v-if="loading">Memprediksi...</span>
        <span v-else>Prediksi Sentimen</span>
      </button>
      <button
        class="secondary"
        @click="handlePreprocess"
        :disabled="!customText.trim() || loading"
      >
        <span v-if="loading">Memproses...</span>
        <span v-else>Hanya Preprocess</span>
      </button>
    </div>

    <!-- Prediction Result -->
    <div v-if="prediction" class="card mt-2">
      <h4>Hasil Prediksi</h4>
      <p>
        Sentimen: <strong :class="getSentimentClass(prediction.prediction)">{{ prediction.prediction }}</strong>
      </p>
      <h5>Probabilitas:</h5>
      <ul>
        <li v-for="(prob, label) in prediction.probabilities" :key="label">
          {{ label }}: <strong>{{ (prob * 100).toFixed(2) }}%</strong>
        </li>
      </ul>
    </div>

    <!-- Example texts -->
    <div class="mt-2" style="padding: 1rem; background: var(--bg-color); border-radius: 8px;">
      <p style="font-weight: 500; margin-bottom: 0.5rem;">Contoh Teks:</p>
      <button
        class="secondary"
        style="width: 100%; margin-bottom: 0.5rem; text-align: left;"
        @click="customText = 'Aplikasi ini sangat membantu, semuanya jadi lebih mudah!'"
      >
        Contoh Positif
      </button>
      <button
        class="secondary"
        style="width: 100%; margin-bottom: 0.5rem; text-align: left;"
        @click="customText = 'Sering error dan lambat, tolong diperbaiki.'"
      >
        Contoh Negatif
      </button>
      <button
        class="secondary"
        style="width: 100%; text-align: left;"
        @click="customText = 'Biasa saja, tidak ada yang spesial.'"
      >
        Contoh Netral
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'CustomTextProcessor',
  props: {
    loading: Boolean,
    prediction: Object,
  },
  emits: ['process', 'predict'],
  setup(props, { emit }) {
    const customText = ref('Aplikasi ini sangat membantu, semuanya jadi lebih mudah!')
    const applyStemming = ref(true)

    const handlePreprocess = () => {
      emit('process', {
        text: customText.value,
        apply_stemming: applyStemming.value
      })
    }
    
    const handlePredict = () => {
      emit('predict', {
        text: customText.value,
        apply_stemming: applyStemming.value
      })
    }

    const getSentimentClass = (sentiment) => {
      if (!sentiment) return ''
      const s = sentiment.toLowerCase()
      if (s === 'positive') return 'text-success'
      if (s === 'negative') return 'text-error'
      return 'text-warning'
    }

    return {
      customText,
      applyStemming,
      handlePreprocess,
      handlePredict,
      getSentimentClass,
    }
  }
}
</script>

<style scoped>
.button-group {
  display: flex;
  gap: 10px;
}
.button-group button {
  flex-grow: 1;
}
.form-group {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}
.text-success {
  color: var(--success-color);
  font-weight: bold;
}
.text-error {
  color: var(--error-color);
  font-weight: bold;
}
.text-warning {
  color: var(--warning-color);
  font-weight: bold;
}
</style>
