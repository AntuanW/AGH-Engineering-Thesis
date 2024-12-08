
function onSubmitUploadPkt() {
    form = document.getElementById("pkt-form");
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // The file has been uploaded successfully
        console.log("File successfully uploaded!");
        populateExtractConfigSelect(JSON.parse(xhr.responseText));
      }
    };

    xhr.open("POST", "/config_upload/upload_pkt", true);

    const formData = new FormData();
    formData.append("file", form.pkt_input.files[0]);
    xhr.send(formData);
}

function getXMLNames() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        populateExtractConfigSelect(JSON.parse(xhr.responseText));
      }
    };

    xhr.open("GET", "/config_upload/list_xml_names", false);
    xhr.send();
}

function getTopologyNames() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        populateMappingSelect(JSON.parse(xhr.responseText));
        populateConfigUploadSelect(JSON.parse(xhr.responseText));
      }
    };

    xhr.open("GET", "/config_upload/list_topology_names", false);
    xhr.send();
}

function getGroupNames() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        populateMappingFormGroups(JSON.parse(xhr.responseText));
        populateConfigUploadFormGroups(JSON.parse(xhr.responseText));
      }
    };

    xhr.open("GET", "/config_upload/list_group_names", false);
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
    select.innerHTML = "";
    for (const obj of response) {
        select.innerHTML += `<option value="${obj._id}">${obj.name}</option>\n`
    }
}

function populateMappingFormGroups(response) {
    span = document.getElementById("mapping-form-groups");
    span.innerHTML = "";
    for (group of response) {
        span.innerHTML += `${group.name}<input type="checkbox" value="${group.name}" name="group">`;
    }
}

function populateConfigUploadSelect(response) {
    select = document.getElementById("config-upload-form-select");
    select.innerHTML = "";
    for (const obj of response) {
        select.innerHTML += `<option value="${obj._id}">${obj.name}</option>\n`
    }
}

function populateConfigUploadFormGroups(response) {
    span = document.getElementById("config-upload-form-groups");
    span.innerHTML = "";
    for (group of response) {
        span.innerHTML += `${group.name}<input type="checkbox" value="${group.name}" name="group">`;
    }
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