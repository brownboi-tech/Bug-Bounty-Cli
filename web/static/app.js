async function postScan() {
  const target = document.getElementById('target').value;
  const fast_mode = document.getElementById('fast').checked;
  const res = await fetch('/scans', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ target, fast_mode })
  });
  const data = await res.json();
  document.getElementById('job-info').innerText = `Started scan #${data.id} (${data.status})`;
  document.getElementById('scan-id').value = data.id;
}

async function getScan() {
  const id = document.getElementById('scan-id').value;
  const res = await fetch(`/scans/${id}`);
  const data = await res.json();
  document.getElementById('scan-status').innerText = JSON.stringify(data, null, 2);
}

async function getReport() {
  const id = document.getElementById('scan-id').value;
  const sev = document.getElementById('severity').value;
  const res = await fetch(`/reports/${id}`);
  const data = await res.json();
  const findings = (data.findings || []).filter(f => sev === 'all' || (f.severity || '').toLowerCase() === sev);
  const list = document.getElementById('findings');
  list.innerHTML = '';
  findings.forEach(f => {
    const li = document.createElement('li');
    li.innerText = `[${f.severity}] ${f.type} @ ${f.location}`;
    list.appendChild(li);
  });
}

document.getElementById('submit').addEventListener('click', postScan);
document.getElementById('check').addEventListener('click', getScan);
document.getElementById('load-report').addEventListener('click', getReport);
