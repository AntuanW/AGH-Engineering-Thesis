
function getObjectNames() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        response = JSON.parse(xhr.responseText)
        populateExtractConfigSelect(response.XMLs);
        populateConfigUploadSelect(response.topologies);
        populateConfigUploadFormGroups(response.groups);
        populateMappingSelect(response.topologies);
        populateMappingFormGroups(response.groups);
      }
    };

    xhr.open("GET", "/config_upload/list_names", true);
    xhr.send();
}


function populateExtractConfigSelect(response) {
    select = document.getElementById("extract-form-select");
    select.innerHTML = "";
    for (const obj of response) {
        select.innerHTML += `<option value="${obj._id}">${obj.name}</option>\n`
    }
}


function populateMappingSelect(response) {
    select = document.getElementById("mapping-form-select");
    ss = ""
    for (const obj of response) {
        ss += `<option value="${obj._id}">${obj.name}</option>\n`
    }
    select.innerHTML = ss;
}

function populateMappingFormGroups(response) {
    span = document.getElementById("mapping-form-groups");
    ss = ""
    for (group of response) {
        ss += `<span>${group.name}</span><input type="checkbox" value="${group.name}" name="group">  `;
    }
    span.innerHTML = ss;
}

function populateConfigUploadSelect(response) {
    select = document.getElementById("config-upload-form-select");
    ss = ""
    for (const obj of response) {
        ss += `<option value="${obj._id}">${obj.name}</option>\n`
    }
    select.innerHTML = ss;
}

function populateConfigUploadFormGroups(response) {
    span = document.getElementById("config-upload-form-groups");
    ss = ""
    for (group of response) {
        ss += `<span>${group.name}</span><input type="checkbox" value="${group.name}" name="group">  `;
    }
    span.innerHTML = ss;
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