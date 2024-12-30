function getObjectNames() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        window.localStorage.setItem("model", xhr.responseText);
        response = JSON.parse(xhr.responseText);
        populateMappingSelects(response);
        populateGroupCheckboxes(response);
        populateGroupSelects(response);
        refreshDownloadDynamicDevices();
      }
    };

    xhr.open("GET", "/config_upload/index_dto", true);
    xhr.send();
}

function populateMappingSelects(response) {
    selects = document.getElementsByClassName("__mapping_select")
    ss = ""
    for (const obj of response.mappings) {
        ss += `<option value="${obj._id}">${obj.name}</option>\n`
    }
    for (select of selects) {
        select.innerHTML = ss;
    }
}

function populateGroupCheckboxes(response) {
    ss = ""
    for (group of response.groups) {
        ss += `<span>${group.lab_group_number}</span><input type="checkbox" value="${group.lab_group_number}" name="group">  `;
    }

    spans = document.getElementsByClassName("__group_checkboxes");
    for (span of spans) {
        span.innerHTML = ss;
    }
}

function populateGroupSelects(response) {
    selects = document.getElementsByClassName("__group_select")
    ss = ""
    for (const group of response.groups) {
        ss += `<option value="${group.lab_group_number}">${group.lab_group_number}</option>\n`
    }
    for (select of selects) {
        select.innerHTML = ss;
    }
}

function getModel() {
    return JSON.parse(window.localStorage.getItem("model"));
}

function getDownloadGroupInfo() {
    group_number = document.getElementById("download-form-select").value;
    model = getModel();
    group = model.groups.find(el => el.lab_group_number == group_number);
    return group;
}

function refreshDownloadDynamicDevices() {
    dynamic_devices_table = document.getElementById("download-dynamic-devices");
    dynamic_devices_table.innerHTML = `
    <thead>
    <tr>
    <td>IP</td>
    <td>Port</td>
    <tr>
    </thead><tbody id="download-dynamic-devices-body"></tbody>`

    addDownloadDynamicDevice();
}

function addDownloadDynamicDevice() {
    group = getDownloadGroupInfo();
    ip = group.rack.config_port_ip_address;
    ports = group.rack.config_ports;
    dynamic_devices_table = document.getElementById("download-dynamic-devices-body");

    row = dynamic_devices_table.insertRow(-1);
    cell1 = row.insertCell(0);
    cell1.innerHTML = `<input name="ip_address" type="text" value="${ip}" />`;

    cell2 = row.insertCell(1);
    html = `<select name="port" form="download-form">`;
    for (port of ports) {
        html += `<option value=${port}>${port}</option>`;
    }
    html += "</select>"
    cell2.innerHTML = html;
}








function onSubmitUploadConfig() {
    form = document.getElementById("config-upload-form");
    mapping_id = form.select.value;

    groups = document.getElementById("config-upload-form-groups");
    group_ids_url = "?"
    for (child of groups.children) {
        if (child.checked) {
            group_ids_url += `group_id=${child.value}&`;
        }
    }

    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {

      }
    };

    xhr.open("POST", `/config_upload/mapping/${mapping_id}/configure/${group_ids_url}`, true);
    xhr.send();
}

function onSubmitDownloadConfig() {
    function processRow(row) {
        let inputs = Array.from(row.querySelectorAll("input, select"));
        console.log(row.querySelectorAll("input, select"));
        console.log(inputs);
        return {
            ip_address: inputs.find(e => e.name == "ip_address").value,
            port: inputs.find(e => e.name == "port").value
        }
    }

    form = document.getElementById("download-form");
    lab_name = form.lab_name.value;
    lab_group = form.lab_group.value;
    dynamic_devices_table = document.getElementById("download-dynamic-devices-body");
    rows = dynamic_devices_table.querySelectorAll("tr");

    payload = {
        lab_name: lab_name,
        lab_group: lab_group,
        devices: []
    }
    for (row of rows) {
        payload.devices.push(processRow(row));
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/config_download/download_configs`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(payload));

}


function onSubmitCombineUploadSteps() {
    // Upload
    form = document.getElementById("pkt-form");
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // TODO update only the following step
        getObjectNames();
      }
    };

    xhr.open("POST", "/config_upload/upload_pkt", false);

    const formData = new FormData();
    formData.append("file", form.pkt_input.files[0]);
    xhr.send(formData);
    const uploadResponse = JSON.parse(xhr.responseText);

    // Extract
    xml_id = uploadResponse.xml_id;

    const xhr2 = new XMLHttpRequest();

    xhr2.onreadystatechange = function() {
      if (xhr2.readyState === 4 && xhr2.status === 200) {
        getObjectNames();
      }
    };

    xhr2.open("GET", `/config_upload/extract_xml/${xml_id}`, false);
    xhr2.send();
    const extractResponse = JSON.parse(xhr2.responseText)

    // Map
    topo_id = extractResponse.topology_id;

    groups = document.getElementById("mapping-form-groups");
    group_ids_url = "?"
    for (child of groups.children) {
        if (child.checked) {
            group_ids_url += `group_id=${child.value}&`;
        }
    }

    const xhr3 = new XMLHttpRequest();

    xhr3.onreadystatechange = function() {
      if (xhr3.readyState === 4 && xhr3.status === 200) {
        getObjectNames();
      }
    };

    xhr3.open("GET", `/config_upload/topologies/${topo_id}/mapping${group_ids_url}`, false);
    xhr3.send();

    // PDFs
    const xhr4 = new XMLHttpRequest();

    xhr4.onreadystatechange = function() {
        if (xhr4.readyState === 4 && xhr4.status === 200) {
            var downloadUrl = URL.createObjectURL(xhr4.response);
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            a.href = downloadUrl;
            a.download = "";
            a.click();  // https://stackoverflow.com/questions/32623731/how-to-make-browser-download-file-from-xhr-request
            a.remove(); // what a pile of garbage that is
        }
    };

    xhr4.open("GET", `/file_export/export_lab_instructions/${topo_id}`, true);
    xhr4.responseType = "blob";
    xhr4.send();
}