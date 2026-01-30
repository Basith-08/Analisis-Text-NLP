<template>
  <div>
    <h3>Train and Evaluate Models</h3>
    <div v-if="!selectedDataset">
      <label for="dataset">Pilih Dataset:</label>
      <select id="dataset" v-model="selectedDataset" @change="loadColumns">
        <option disabled value="">-- Pilih salah satu --</option>
        <option v-for="ds in datasets" :key="ds" :value="ds">{{ ds }}</option>
      </select>
    </div>

    <div v-if="selectedDataset && columns.length > 0">
      <p>Dataset: <strong>{{ selectedDataset }}</strong></p>
      <div class="form-group">
        <label for="text_column">Pilih Kolom Teks (Fitur):</label>
        <select id="text_column" v-model="selectedTextColumn">
          <option v-for="col in columns" :key="col" :value="col">{{ col }}</option>
        </select>
      </div>

      <div class="form-group">
        <label for="label_column">Pilih Kolom Label (Target):</label>
        <select id="label_column" v-model="selectedLabelColumn">
          <option v-for="col in columns" :key="col" :value="col">{{ col }}</option>
        </select>
      </div>
      
      <div class="form-group">
        <input type="checkbox" id="apply_stemming" v-model="applyStemming" />
        <label for="apply_stemming" style="margin-left: 8px;">Terapkan Stemming</label>
      </div>

      <button @click="startTraining" :disabled="loading || !selectedTextColumn || !selectedLabelColumn">
        <span v-if="loading">Training...</span>
        <span v-else>Mulai Training & Evaluasi</span>
      </button>
      <button @click="reset" class="secondary" style="margin-left: 10px;">Ganti Dataset</button>
    </div>
    
    <div v-if="error" class="alert alert-error" style="margin-top: 1rem;">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'TrainingView',
  props: {
    datasets: Array,
    loading: Boolean,
  },
  emits: ['train', 'load-columns'],
  setup(props, { emit }) {
    const selectedDataset = ref('');
    const columns = ref([]);
    const selectedTextColumn = ref(null);
    const selectedLabelColumn = ref(null);
    const applyStemming = ref(true);
    const error = ref('');

    const loadColumns = async () => {
      if (!selectedDataset.value) return;
      try {
        const response = await fetch('/api/load-dataset', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filename: selectedDataset.value }),
        });
        const data = await response.json();
        if (data.status === 'success') {
          columns.value = data.columns;
          if(data.columns.length > 0) {
            selectedTextColumn.value = data.columns[0];
            selectedLabelColumn.value = data.columns.length > 1 ? data.columns[1] : data.columns[0];
          }
        } else {
          error.value = `Error loading columns: ${data.message}`;
        }
      } catch (e) {
        error.value = `Error: ${e.message}`;
      }
    };

    const startTraining = () => {
      if (!selectedTextColumn.value || !selectedLabelColumn.value) {
        error.value = "Silakan pilih kolom teks dan label.";
        return;
      }
      if (selectedTextColumn.value === selectedLabelColumn.value) {
        error.value = "Kolom teks dan kolom label tidak boleh sama.";
        return;
      }
      error.value = '';
      emit('train', {
        filename: selectedDataset.value,
        text_column: selectedTextColumn.value,
        label_column: selectedLabelColumn.value,
        apply_stemming: applyStemming.value,
      });
    };
    
    const reset = () => {
      selectedDataset.value = '';
      columns.value = [];
      selectedTextColumn.value = null;
      selectedLabelColumn.value = null;
      error.value = '';
    }

    return {
      selectedDataset,
      columns,
      selectedTextColumn,
      selectedLabelColumn,
      applyStemming,
      error,
      loadColumns,
      startTraining,
      reset
    };
  },
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
</style>
