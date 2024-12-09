function getObjectNames() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        response = JSON.parse(xhr.responseText)
        populateXMLSelects(response);
        populateTopologySelects(response);
        populateGroupPickers(response);
      }
    };

    xhr.open("GET", "/config_upload/list_names", true);
    xhr.send();
}



function populateXMLSelects(response) {
    selects = document.getElementsByClassName("__xml_select");
    ss = "";
    for (const obj of response.XMLs) {
        ss += `<option value="${obj._id}">${obj.name}</option>\n`;
    }
    for (select of selects) {
        select.innerHTML = ss;
    }
}

function populateTopologySelects(response) {
    selects = document.getElementsByClassName("__topo_select")
    ss = ""
    for (const obj of response.topologies) {
        ss += `<option value="${obj._id}">${obj.name}</option>\n`
    }
    for (select of selects) {
        select.innerHTML = ss;
    }
}

function populateGroupPickers(response) {
    ss = ""
    for (group of response.groups) {
        ss += `<span>${group.name}</span><input type="checkbox" value="${group.name}" name="group">  `;
    }

    spans = document.getElementsByClassName("__group_select");
    for (span of spans) {
        span.innerHTML = ss;
    }
}





function onSubmitUploadPkt() {
    form = document.getElementById("pkt-form");
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        populateExtractConfigSelect(JSON.parse(xhr.responseText));
      }
    };

    xhr.open("POST", "/config_upload/upload_pkt", true);

    const formData = new FormData();
    formData.append("file", form.pkt_input.files[0]);
    xhr.send(formData);
}


function onSubmitExtractConfig() {
    form = document.getElementById("extract-form");
    action = form.select.value;

    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        populateMappingSelect(JSON.parse(xhr.responseText));
        populateConfigUploadSelect(JSON.parse(xhr.responseText));
      }
    };

    xhr.open("GET", `/config_upload/extract_xml/${action}`, true);
    xhr.send();
}


function onSubmitGetMapping() {
    form = document.getElementById("mapping-form");
    topo_id = form.select.value;

    groups = document.getElementById("mapping-form-groups");
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

    xhr.open("GET", `/config_upload/topologies/${topo_id}/mapping${group_ids_url}`, true);
    xhr.send();
}


function onSubmitUploadConfig() {
    form = document.getElementById("config-upload-form");
    topo_id = form.select.value;

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

    xhr.open("POST", `/config_upload/topologies/${topo_id}/configure/${group_ids_url}`, true);
    xhr.send();
}


function onSubmitGeneratePDF() {
    form = document.getElementById("instruction-form");
    topo_id = form.select.value;

    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var downloadUrl = URL.createObjectURL(xhr.response);
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            a.href = downloadUrl;
            a.download = "";
            a.click();  // https://stackoverflow.com/questions/32623731/how-to-make-browser-download-file-from-xhr-request
            a.remove(); // what a pile of garbage that is
        }
    };

    xhr.open("GET", `/file_export/export_student_instructions/${topo_id}`, true);
    xhr.responseType = "blob";
    xhr.send();
}