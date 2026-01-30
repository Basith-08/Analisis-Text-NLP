<template>
  <div class="card" v-if="results">
    <h2>Hasil Training & Evaluasi</h2>

    <div class="alert alert-success">
      Model terbaik: <strong>{{ results.best_model_summary.model }}</strong> dengan
      vektorisasi <strong>{{ results.best_model_summary.vectorization }}</strong>
      dan akurasi <strong>{{ (results.best_model_summary.accuracy * 100).toFixed(2) }}%</strong>.
    </div>

    <div v-for="(vec_results, vec_name) in results.results" :key="vec_name" style="margin-top: 2rem;">
      <h3>Metode Vektorisasi: {{ vec_name.toUpperCase() }}</h3>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Model</th>
              <th>Akurasi</th>
              <th>Presisi</th>
              <th>Recall</th>
              <th>F1-Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(model_results, model_name) in vec_results" :key="model_name">
              <td>{{ model_name }}</td>
              <td>{{ (model_results.accuracy * 100).toFixed(2) }}%</td>
              <td>{{ (model_results.precision * 100).toFixed(2) }}%</td>
              <td>{{ (model_results.recall * 100).toFixed(2) }}%</td>
              <td>{{ (model_results.f1_score * 100).toFixed(2) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h4>Confusion Matrices ({{ vec_name.toUpperCase() }})</h4>
      <div class="cm-grid">
        <div v-for="(model_results, model_name) in vec_results" :key="model_name" class="cm-container">
          <h5>{{ model_name }}</h5>
          <table class="cm-table">
             <thead>
              <tr>
                <th></th>
                <th v-for="label in results.label_names" :key="label">{{ label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in model_results.confusion_matrix" :key="i">
                <th>{{ results.label_names[i] }}</th>
                <td v-for="(cell, j) in row" :key="j" :style="getCellStyle(cell, model_results.confusion_matrix)">
                  {{ cell }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultsView',
  props: {
    results: Object,
  },
  setup() {
    const getCellStyle = (value, matrix) => {
      const max = Math.max(...matrix.flat());
      const opacity = value === 0 ? 0.1 : Math.max(0.2, value / max);
      return {
        backgroundColor: `rgba(33, 150, 243, ${opacity})`,
      };
    };
    
    return {
      getCellStyle
    }
  }
};
</script>

<style scoped>
.cm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
.cm-container {
  text-align: center;
}
.cm-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}
.cm-table th, .cm-table td {
  border: 1px solid var(--border-color);
  padding: 0.5rem;
  text-align: center;
}
.cm-table th {
  background-color: var(--background-secondary);
}
</style>
