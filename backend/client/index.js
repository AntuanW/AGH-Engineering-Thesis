
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

function populateExtractConfigSelect(response) {
    select = document.getElementById("extract-form-select");
    for (const obj of response) {
        select.innerHTML += `<option value="${obj._id}">${obj.name}</option>\n`
    }
}


function populateMapping(response) {
    console.log(response);
}


function onSubmitExtractConfig() {
    form = document.getElementById("extract-form");
    action = form.select.value;

    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        populateMapping(JSON.parse(xhr.responseText));
      }
    };

    xhr.open("GET", `/config_upload/extract_xml/${action}`, true);
    xhr.send();
}