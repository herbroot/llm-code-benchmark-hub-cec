async function loadScores() {
  const res = await fetch('./data/scores.json');
  if (!res.ok) throw new Error('Failed to load scores.json');
  return res.json();
}

function toText(v) {
  if (v === null || v === undefined || v === '') return '-';
  return String(v);
}

function render(rows) {
  const body = document.getElementById('scoreBody');
  body.innerHTML = '';

  rows.forEach((r) => {
    const tr = document.createElement('tr');
    const sourceCell = r.source_url && r.source_url !== 'TBD'
      ? `<a href="${r.source_url}" target="_blank" rel="noopener noreferrer">${toText(r.source_name)}</a>`
      : toText(r.source_name);

    tr.innerHTML = `
      <td>${toText(r.benchmark)}</td>
      <td>${toText(r.metric)}</td>
      <td>${toText(r.model_family)}</td>
      <td>${toText(r.model_name)}</td>
      <td>${toText(r.score)}</td>
      <td>${sourceCell}</td>
      <td>${toText(r.source_date)}</td>
    `;
    body.appendChild(tr);
  });
}

function renderChips(rows) {
  const chips = document.getElementById('benchmarkChips');
  const names = [...new Set(rows.map((r) => r.benchmark).filter(Boolean))].sort();
  chips.innerHTML = names.map((n) => `<span>${n}</span>`).join('');
}

function applyFilter(rows, keyword) {
  const k = keyword.trim().toLowerCase();
  if (!k) return rows;
  return rows.filter((r) => Object.values(r).join(' ').toLowerCase().includes(k));
}

(async function main() {
  try {
    const payload = await loadScores();
    const allRows = payload.rows || [];
    renderChips(allRows);
    render(allRows);

    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', () => {
      const filtered = applyFilter(allRows, searchInput.value);
      render(filtered);
    });
  } catch (err) {
    const body = document.getElementById('scoreBody');
    body.innerHTML = `<tr><td colspan="7">${err.message}</td></tr>`;
  }
})();
