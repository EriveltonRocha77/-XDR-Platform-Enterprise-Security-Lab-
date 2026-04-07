document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.querySelectorAll('.app-view').forEach(v => v.classList.remove('active'));
        e.currentTarget.classList.add('active');
        const viewId = e.currentTarget.getAttribute('data-view');
        document.getElementById(`view-${viewId}`).classList.add('active');
    });
});

function typeWriterEffect(element, text, speed = 8) {
    element.innerHTML = "";
    let i = 0;
    element.classList.add('typing');
    return new Promise(resolve => {
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                const randSpeed = speed + Math.random() * 15;
                setTimeout(type, randSpeed);
            } else {
                element.classList.remove('typing');
                resolve();
            }
        }
        type();
    });
}

async function runBackendModule(moduleName, target = "") {
    const btn = document.querySelector(`#view-${moduleName} .action-run-btn`);
    const outputArea = document.getElementById(`output-${moduleName}`);
    const originalText = btn.innerHTML;
    
    btn.innerHTML = `<span style="animation: blink 1s infinite">EXECUTANDO...</span>`;
    btn.style.borderColor = "var(--warning)";
    btn.style.color = "var(--warning)";
    btn.style.boxShadow = "0 0 20px rgba(255,184,0,0.4)";
    outputArea.innerHTML = "INICIALIZANDO MOTOR CIBERNÉTICO...\nESTABELECENDO CONEXÃO DE REDE TLS...\nINJETANDO KERNEL PAYLOADS...";

    try {
        const url = `http://localhost:8000/api/v1/run/${moduleName}?target=${encodeURIComponent(target)}`;
        const response = await fetch(url);
        const data = await response.json();
        
        btn.style.borderColor = "var(--cyan)";
        btn.style.color = "var(--cyan)";
        btn.style.boxShadow = "none";
        
        let outText = "";
        if (data.output) {
            outText = `[+] TRANSMISSÃO DE DADOS RECEBIDA.\n[+] PROCESSAMENTO MILITAR CONCLUÍDO:\n${data.output}`;
        } else if (data.error) {
            btn.style.borderColor = "var(--red)";
            btn.style.color = "var(--red)";
            btn.style.boxShadow = "0 0 20px rgba(255,42,42,0.4)";
            outText = `[ERRO CRÍTICO NO SISTEMA]\n${data.error}`;
        } else {
            outText = `[+] ANÁLISE INTERNA CONCLUÍDA:\n${JSON.stringify(data, null, 2)}`;
        }
        await typeWriterEffect(outputArea, outText);
        
    } catch (err) {
        btn.style.borderColor = "var(--red)";
        btn.style.color = "var(--red)";
        btn.style.boxShadow = "0 0 20px rgba(255,42,42,0.4)";
        typeWriterEffect(outputArea, `[FALHA DE COMUNICAÇÃO FATAL]\nO Sistema Integrado (SIEM) não respondeu aos comandos HTTP.\nCertifique-se de que a malha de Containers Docker está online.\nErro Gerado: ${err.message}`);
    } finally {
        btn.innerHTML = originalText;
    }
}

async function fetchLiveThreats() {
    const table = document.querySelector('#liveFeedTable tbody');
    table.innerHTML = "<tr><td colspan='4' style='color:var(--cyan)'>Buscando pacotes no banco de dados XDR...</td></tr>";
    
    try {
        const response = await fetch("http://localhost:8000/api/v1/threats");
        const data = await response.json();
        
        document.getElementById('stat-total').innerText = data.total_events;
        document.getElementById('stat-danger').innerText = data.incidents.filter(i => i.severity === 'HIGH' || i.severity === 'CRITICAL').length;
        document.getElementById('backend-status').innerText = 'Auditoria Ativa';
        document.getElementById('backend-status').style.color = 'var(--cyan)';
        document.getElementById('backend-status').style.textShadow = '0 0 10px var(--cyan)';
        
        table.innerHTML = "";
        if (data.incidents.length === 0) {
            table.innerHTML = "<tr><td colspan='4' style='color:var(--text)'>Nenhum incidente interceptado na sessão atual do Laboratório.</td></tr>";
            return;
        }
        
        data.incidents.slice(0, 15).forEach(inc => {
            let color = inc.severity === 'HIGH' || inc.severity === 'CRITICAL' ? 'var(--red)' : inc.severity === 'MEDIUM' ? 'var(--warning)' : 'var(--text)';
            table.innerHTML += `
                <tr style="color: ${color}">
                    <td><span style="opacity:0.7">${new Date(inc.timestamp).toLocaleTimeString()}</span></td>
                    <td><b>${inc.engine.toUpperCase()}</b></td>
                    <td>[${inc.severity}]</td>
                    <td>${JSON.stringify(inc.data).substring(0, 100)}...</td>
                </tr>
            `;
        });
    } catch (err) {
        document.getElementById('backend-status').innerText = 'Desconectado / Falha no Ring Central';
        document.getElementById('backend-status').style.color = 'var(--red)';
        document.getElementById('backend-status').style.textShadow = '0 0 10px var(--red)';
        table.innerHTML = `<tr><td colspan='4' style="color:var(--red);">[CRÍTICO] Não foi possível encontrar a rota do servidor Backend (Porta 8000).</td></tr>`;
    }
}

setTimeout(fetchLiveThreats, 800);
