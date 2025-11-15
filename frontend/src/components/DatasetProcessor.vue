<template>
  <div>
    <h3>Proses Dataset</h3>

    <!-- Upload Section -->
    <div class="mb-2" style="padding: 1rem; background: var(--bg-color); border-radius: 8px; border: 2px dashed var(--border-color);">
      <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">
        Upload Dataset Baru:
      </label>

      <div class="flex" style="gap: 0.5rem; align-items: center;">
        <input
          type="file"
          ref="fileInput"
          @change="onFileSelect"
          accept=".csv"
          style="flex: 1;"
        />
        <button
          @click="uploadFile"
          :disabled="!selectedFile || uploading"
          class="secondary"
          style="width: auto;"
        >
          <span v-if="uploading" class="loading"></span>
          <span v-else>Upload</span>
        </button>
      </div>

      <small style="color: var(--text-secondary); display: block; margin-top: 0.5rem;">
        Format: CSV (maks. 16MB)
      </small>

      <!-- Upload Status -->
      <div v-if="uploadMessage" class="mt-1" :class="uploadSuccess ? 'alert alert-success' : 'alert alert-error'" style="padding: 0.5rem;">
        {{ uploadMessage }}
      </div>
    </div>

    <!-- Dataset Selection -->
    <div class="mb-2">
      <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">
        Pilih Dataset:
      </label>
      <div class="flex" style="gap: 0.5rem;">
        <select v-model="selectedDataset" @change="onDatasetChange" style="flex: 1;">
          <option value="">-- Pilih dataset --</option>
          <option v-for="dataset in datasets" :key="dataset" :value="dataset">
            {{ dataset }}
          </option>
        </select>
        <button @click="refreshDatasets" class="secondary" style="width: auto;">
          &#x21bb; Refresh
        </button>
      </div>
    </div>

    <!-- Column Selection -->
    <div v-if="datasetInfo" class="mb-2">
      <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">
        Pilih Kolom Teks:
      </label>
      <select v-model="selectedColumn">
        <option value="">-- Pilih kolom --</option>
        <option v-for="col in datasetInfo.columns" :key="col" :value="col">
          {{ col }}
        </option>
      </select>
    </div>

    <!-- Limit Selection -->
    <div v-if="datasetInfo" class="mb-2">
      <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">
        Jumlah Data yang Diproses:
      </label>
      <input
        type="number"
        v-model.number="limit"
        min="1"
        :max="datasetInfo.total_rows"
        placeholder="Jumlah baris"
      />
      <small style="color: var(--text-secondary); display: block; margin-top: 0.25rem;">
        Total baris dalam dataset: {{ datasetInfo.total_rows }}
      </small>
    </div>

    <!-- Dataset Preview -->
    <div v-if="datasetInfo && datasetInfo.preview.length > 0" class="mb-2">
      <h4>Preview Dataset:</h4>
      <div class="table-container" style="max-height: 300px; overflow-y: auto;">
        <table>
          <thead>
            <tr>
              <th v-for="col in datasetInfo.columns" :key="col">{{ col }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in datasetInfo.preview.slice(0, 5)" :key="idx">
              <td v-for="col in datasetInfo.columns" :key="col" style="font-size: 0.85em;">
                {{ truncate(String(row[col] || ''), 50) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Process Button -->
    <button
      @click="processDataset"
      :disabled="!selectedDataset || !selectedColumn || loading"
      style="width: 100%;"
    >
      <span v-if="loading" class="loading"></span>
      <span v-else>Proses Dataset</span>
    </button>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'DatasetProcessor',
  props: {
    datasets: Array,
    loading: Boolean
  },
  emits: ['load-datasets', 'process'],
  setup(props, { emit }) {
    const selectedDataset = ref('')
    const selectedColumn = ref('')
    const datasetInfo = ref(null)
    const limit = ref(50)
    const selectedFile = ref(null)
    const uploading = ref(false)
    const uploadMessage = ref('')
    const uploadSuccess = ref(false)
    const fileInput = ref(null)

    const onDatasetChange = async () => {
      if (!selectedDataset.value) {
        datasetInfo.value = null
        return
      }

      try {
        const response = await fetch('/api/load-dataset', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filename: selectedDataset.value })
        })

        const data = await response.json()

        if (data.status === 'success') {
          datasetInfo.value = data
          // Auto-select first text column if available
          const textColumns = ['comment_text', 'video_caption', 'text', 'content']
          const foundCol = data.columns.find(col =>
            textColumns.some(tc => col.toLowerCase().includes(tc))
          )
          if (foundCol) {
            selectedColumn.value = foundCol
          }
        } else {
          alert('Error: ' + data.message)
        }
      } catch (error) {
        alert('Error loading dataset: ' + error.message)
      }
    }

    const processDataset = () => {
      emit('process', {
        filename: selectedDataset.value,
        text_column: selectedColumn.value,
        limit: limit.value
      })
    }

    const truncate = (text, maxLength) => {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    }

    const onFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        // Validate file type
        if (!file.name.endsWith('.csv')) {
          uploadMessage.value = 'Hanya file CSV yang diperbolehkan'
          uploadSuccess.value = false
          selectedFile.value = null
          return
        }

        // Validate file size (16MB)
        if (file.size > 16 * 1024 * 1024) {
          uploadMessage.value = 'Ukuran file maksimal 16MB'
          uploadSuccess.value = false
          selectedFile.value = null
          return
        }

        selectedFile.value = file
        uploadMessage.value = ''
      }
    }

    const uploadFile = async () => {
      if (!selectedFile.value) return

      try {
        uploading.value = true
        uploadMessage.value = ''

        const formData = new FormData()
        formData.append('file', selectedFile.value)

        const response = await fetch('/api/upload-dataset', {
          method: 'POST',
          body: formData
        })

        const data = await response.json()

        if (data.status === 'success') {
          uploadMessage.value = data.message
          uploadSuccess.value = true

          // Clear file input
          selectedFile.value = null
          if (fileInput.value) {
            fileInput.value.value = ''
          }

          // Refresh datasets list
          emit('load-datasets')

          // Auto-select uploaded dataset
          setTimeout(() => {
            selectedDataset.value = data.filename
            onDatasetChange()
          }, 500)
        } else {
          uploadMessage.value = data.message
          uploadSuccess.value = false
        }
      } catch (error) {
        uploadMessage.value = 'Error uploading file: ' + error.message
        uploadSuccess.value = false
      } finally {
        uploading.value = false
      }
    }

    const refreshDatasets = () => {
      emit('load-datasets')
      uploadMessage.value = 'Dataset list refreshed'
      uploadSuccess.value = true
      setTimeout(() => {
        uploadMessage.value = ''
      }, 2000)
    }

    return {
      selectedDataset,
      selectedColumn,
      datasetInfo,
      limit,
      selectedFile,
      uploading,
      uploadMessage,
      uploadSuccess,
      fileInput,
      onDatasetChange,
      processDataset,
      truncate,
      onFileSelect,
      uploadFile,
      refreshDatasets
    }
  }
}
</script>
