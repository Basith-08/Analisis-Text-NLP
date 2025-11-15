<template>
  <div id="app">
    <header class="card">
      <h1>Analisis Text NLP - Preprocessing Tool</h1>
      <p style="color: var(--text-secondary)">
        Tool untuk preprocessing teks menggunakan Python (Pandas, NumPy, NLTK)
      </p>
    </header>

    <!-- Connection Status -->
    <div v-if="backendStatus.error" class="alert alert-error">
      {{ backendStatus.message }}
    </div>
    <div v-else-if="backendStatus.connected" class="alert alert-success">
      Backend terhubung
    </div>

    <!-- Tab Navigation -->
    <div class="card">
      <div class="flex" style="border-bottom: 2px solid var(--border-color); margin-bottom: 1rem;">
        <button
          :class="activeTab === 'dataset' ? 'primary' : 'secondary'"
          @click="activeTab = 'dataset'"
        >
          Dataset Processing
        </button>
        <button
          :class="activeTab === 'custom' ? 'primary' : 'secondary'"
          @click="activeTab = 'custom'"
        >
          Custom Text
        </button>
      </div>

      <!-- Dataset Tab -->
      <div v-if="activeTab === 'dataset'">
        <DatasetProcessor
          :datasets="datasets"
          :loading="loading"
          @load-datasets="loadDatasets"
          @process="processDataset"
        />
      </div>

      <!-- Custom Text Tab -->
      <div v-else>
        <CustomTextProcessor
          :loading="loading"
          @process="processCustomText"
        />
      </div>
    </div>

    <!-- Results -->
    <div v-if="results.length > 0" class="card">
      <h2>Hasil Preprocessing</h2>
      <p style="color: var(--text-secondary); margin-bottom: 1rem;">
        Total data diproses: <strong>{{ results.length }}</strong>
      </p>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width: 50px;">No</th>
              <th style="width: 30%;">Teks Asli</th>
              <th style="width: 25%;">Teks Bersih</th>
              <th style="width: 20%;">Tokens</th>
              <th style="width: 20%;">Filtered Tokens</th>
              <th style="width: 100px;">Jumlah</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in results" :key="result.id">
              <td>{{ result.id }}</td>
              <td style="font-size: 0.9em; color: var(--text-secondary);">
                {{ truncate(result.original, 100) }}
              </td>
              <td style="font-size: 0.9em;">
                {{ truncate(result.cleaned, 100) }}
              </td>
              <td>
                <div style="max-height: 100px; overflow-y: auto; font-size: 0.85em;">
                  <span v-for="(token, idx) in result.tokens" :key="idx" class="badge badge-primary" style="margin: 2px;">
                    {{ token }}
                  </span>
                </div>
              </td>
              <td>
                <div style="max-height: 100px; overflow-y: auto; font-size: 0.85em;">
                  <span v-for="(token, idx) in result.filtered_tokens" :key="idx" class="badge badge-success" style="margin: 2px;">
                    {{ token }}
                  </span>
                </div>
              </td>
              <td>
                <span class="badge badge-warning">{{ result.filtered_count }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import DatasetProcessor from './components/DatasetProcessor.vue'
import CustomTextProcessor from './components/CustomTextProcessor.vue'

export default {
  name: 'App',
  components: {
    DatasetProcessor,
    CustomTextProcessor
  },
  setup() {
    const activeTab = ref('dataset')
    const backendStatus = ref({ connected: false, error: false, message: '' })
    const datasets = ref([])
    const loading = ref(false)
    const results = ref([])

    // Check backend health
    const checkBackend = async () => {
      try {
        const response = await fetch('/api/health')
        const data = await response.json()
        if (data.status === 'ok') {
          backendStatus.value = { connected: true, error: false, message: '' }
        }
      } catch (error) {
        backendStatus.value = {
          connected: false,
          error: true,
          message: 'Backend tidak dapat terhubung. Pastikan server Python berjalan di port 5000.'
        }
      }
    }

    // Load available datasets
    const loadDatasets = async () => {
      try {
        loading.value = true
        const response = await fetch('/api/datasets')
        const data = await response.json()
        if (data.status === 'success') {
          datasets.value = data.datasets
        }
      } catch (error) {
        console.error('Error loading datasets:', error)
      } finally {
        loading.value = false
      }
    }

    // Process dataset
    const processDataset = async (payload) => {
      try {
        loading.value = true
        results.value = []

        const response = await fetch('/api/preprocess', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })

        const data = await response.json()

        if (data.status === 'success') {
          results.value = data.results
        } else {
          alert('Error: ' + data.message)
        }
      } catch (error) {
        alert('Error memproses dataset: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // Process custom text
    const processCustomText = async (text) => {
      try {
        loading.value = true
        results.value = []

        const response = await fetch('/api/preprocess-custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        })

        const data = await response.json()

        if (data.status === 'success') {
          results.value = [{
            id: 1,
            original: data.original,
            cleaned: data.cleaned,
            tokens: data.tokens,
            filtered_tokens: data.filtered_tokens,
            token_count: data.token_count,
            filtered_count: data.filtered_count
          }]
        } else {
          alert('Error: ' + data.message)
        }
      } catch (error) {
        alert('Error memproses text: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // Utility function to truncate text
    const truncate = (text, maxLength) => {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    }

    onMounted(() => {
      checkBackend()
      loadDatasets()
    })

    return {
      activeTab,
      backendStatus,
      datasets,
      loading,
      results,
      loadDatasets,
      processDataset,
      processCustomText,
      truncate
    }
  }
}
</script>
