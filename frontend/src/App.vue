<template>
  <div id="app">
    <header class="card">
      <h1>Analisis Sentimen & Preprocessing NLP</h1>
      <p style="color: var(--text-secondary)">
        Tool untuk preprocessing, training model klasifikasi, dan prediksi sentimen.
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
          @click="switchTab('dataset')"
        >
          Preprocessing
        </button>
        <button
          :class="activeTab === 'training' ? 'primary' : 'secondary'"
          @click="switchTab('training')"
        >
          Training & Evaluasi
        </button>
        <button
          :class="activeTab === 'predict' ? 'primary' : 'secondary'"
          @click="switchTab('predict')"
        >
          Prediksi Teks
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
      
      <!-- Training Tab -->
      <div v-if="activeTab === 'training'">
        <TrainingView
          :datasets="datasets"
          :loading="trainingLoading"
          @train="trainAndEvaluate"
        />
      </div>

      <!-- Predict Tab -->
      <div v-if="activeTab === 'predict'">
        <CustomTextProcessor
          :loading="loading"
          :prediction="predictionResult"
          @process="processCustomText"
          @predict="predictText"
        />
      </div>
    </div>

    <!-- Preprocessing Results -->
    <div v-if="results.length > 0 && activeTab === 'dataset'" class="card">
      <h2>Hasil Preprocessing</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width: 50px;">No</th>
              <th style="width: 30%;">Teks Asli</th>
              <th style="width: 25%;">Teks Bersih</th>
              <th style="width: 20%;">Tokens</th>
              <th style="width: 20%;">Filtered Tokens</th>
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
    
    <!-- Preprocessing result for custom text -->
    <div v-if="results.length > 0 && activeTab === 'predict'" class="card">
        <h2>Hasil Preprocessing</h2>
        <p>Teks Asli: <strong>{{ results[0].original }}</strong></p>
        <p>Teks Bersih: <strong>{{ results[0].cleaned }}</strong></p>
        <p>Tokens Final (setelah stopword & stemming):</p>
        <div>
            <span v-for="(token, idx) in results[0].filtered_tokens" :key="idx" class="badge badge-success" style="margin: 2px;">
                {{ token }}
            </span>
        </div>
    </div>


    <!-- Training Results -->
    <ResultsView v-if="trainingResults && activeTab === 'training'" :results="trainingResults" />

  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import DatasetProcessor from './components/DatasetProcessor.vue'
import CustomTextProcessor from './components/CustomTextProcessor.vue'
import TrainingView from './components/TrainingView.vue'
import ResultsView from './components/ResultsView.vue'


export default {
  name: 'App',
  components: {
    DatasetProcessor,
    CustomTextProcessor,
    TrainingView,
    ResultsView,
  },
  setup() {
    const activeTab = ref('dataset')
    const backendStatus = ref({ connected: false, error: false, message: '' })
    const datasets = ref([])
    const loading = ref(false)
    const trainingLoading = ref(false)
    const results = ref([])
    const trainingResults = ref(null)
    const predictionResult = ref(null)

    const switchTab = (tabName) => {
        activeTab.value = tabName
        // Clear results when switching tabs
        results.value = []
        if (tabName !== 'training') trainingResults.value = null
        if (tabName !== 'predict') predictionResult.value = null
    }

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

    // Process dataset for preprocessing view
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
    
    // Train and evaluate models
    const trainAndEvaluate = async (payload) => {
      try {
        trainingLoading.value = true
        trainingResults.value = null
        const response = await fetch('/api/train_evaluate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const responseText = await response.text();
        try {
          const data = JSON.parse(responseText);
          if (data.status === 'success') {
            trainingResults.value = data
          } else {
            alert('Error: ' + data.message)
          }
        } catch (e) {
          console.error("Failed to parse JSON:", responseText);
          alert('An error occurred during training. The server response was not valid JSON. Check the console for more details.');
        }

      } catch (error) {
        alert('Error during training: ' + error.message)
      } finally {
        trainingLoading.value = false
      }
    }

    // Process custom text for preprocessing view
    const processCustomText = async (payload) => {
      try {
        loading.value = true
        results.value = []
        predictionResult.value = null
        const response = await fetch('/api/preprocess-custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
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

    // Predict sentiment for custom text
    const predictText = async (payload) => {
        try {
            loading.value = true;
            predictionResult.value = null;
            results.value = [];
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            if (data.status === 'success') {
                predictionResult.value = data;
            } else {
                alert('Error: ' + data.message);
            }
        } catch (error) {
            alert('Error predicting: ' + error.message);
        } finally {
            loading.value = false;
        }
    };

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
      trainingLoading,
      results,
      trainingResults,
      predictionResult,
      switchTab,
      loadDatasets,
      processDataset,
      trainAndEvaluate,
      processCustomText,
      predictText,
      truncate
    }
  }
}
</script>
