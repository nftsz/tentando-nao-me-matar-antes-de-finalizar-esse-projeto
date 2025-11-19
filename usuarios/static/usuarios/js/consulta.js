async function consultarHistorico() {
    const cpfInput = document.getElementById("cpf_search");
    const msg = document.getElementById("statusBusca");
    const areaResultados = document.getElementById("resultado_area");
    const tbody = document.getElementById("tabela_corpo");

    // Selecionamos o container do título
    const tituloContainer = document.getElementById("titulo_container");

    const cpf = cpfInput.value.trim();

    if (!cpf) {
        msg.textContent = "Por favor, digite um CPF.";
        msg.className = "search-status status-warning";
        areaResultados.style.display = "none";
        return;
    }

    msg.textContent = "Buscando dados...";
    msg.className = "search-status status-info";
    tbody.innerHTML = "";
    tituloContainer.innerHTML = ""; // Limpa título anterior
    areaResultados.style.display = "none";

    try {
        const response = await fetch(`/api/buscar-ocis/?cpf=${cpf}`);
        const data = await response.json();

        if (data.found) {
            msg.textContent = "Resultados encontrados.";
            msg.className = "search-status status-success";

            tituloContainer.innerHTML = `<h2 class="resultados-title">${data.paciente.nome} (${data.paciente.cpf})</h2>`;
            areaResultados.style.display = "block";

            if (data.ocis.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5">Este paciente não possui nenhuma OCI registrada.</td></tr>`;
            } else {
                data.ocis.forEach(oci => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                            <td>${oci.codigo_oci}</td>
                            <td>${oci.nome_oci}</td>
                            <td>${oci.tipo_oci}</td>
                            <td>${oci.profissional}</td>
                            <td>${oci.data_abertura}</td>
                            <td>${oci.data_conclusao}</td>
                            <td class="${oci.classe_status}">${oci.data_limite}</td>
                        `;
                    tbody.appendChild(tr);
                });
            }

        } else {
            msg.textContent = data.message || "Paciente não encontrado.";
            msg.className = "search-status status-warning";
        }

    } catch (error) {
        console.error(error);
        msg.textContent = "Erro ao consultar servidor.";
        msg.className = "search-status status-warning";
    }
}

document.getElementById("cpf_search").addEventListener("keypress", function (event) {
    if (event.key === "Enter") consultarHistorico();
});