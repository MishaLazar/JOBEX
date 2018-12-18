(function () {

    var jobsTable = $("#jobs_table");
    var rulesTable = $("#rules_table");
    var submitButton = $("#submit_button");
    var backButton = $("#back_button")
    var devicesSelect = $("#devices_select");
    var endDateSelector = $(".datepicker").datepicker({minDate : 0});

    function dropdownSelect() {
        var device_id = $("#devices_select").val();
        var url = "/ps/tools/apg_tool/rules/" + device_id;
        location.href = url;
    }

    function sendRequest(url, jsonData, callback) {
        var xhr = new XMLHttpRequest();
        var update_status_span = $('#status');
        xhr.open('POST', url);

        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if ([401, 502].includes(xhr.status) || xhr.response.includes('Login')) {
                update_status_span.css('color', 'red');
                update_status_span.text('Unauthorised. Refresh the page to login again.');
            }
            else if (xhr.status === 200) {
            }
            else {
                update_status_span.css('color', 'red');
                update_status_span.text(xhr.response);
            }

            if (callback) {
                callback(xhr.response);
            }
        };

        xhr.send(JSON.stringify(jsonData));
    }

    function submitButtonClick() {

        var data_to_send = {};
        var device_id = window.location.pathname.split('/')[5];
        var url = "/ps/tools/apg_tool/submit";
        var main_page = "/ps/tools/apg_tool"
        var rules_checkboxes = $(".rule_checkbox");
        var rules_datepickers = $(".datepicker");
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();
        var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds

        data_to_send['device_id'] = device_id;
        data_to_send['rules_ids'] = [];
        data_to_send['durations'] = [];

        for (var i=0; i <rules_checkboxes.length; i++){
            var rule_checkbox = rules_checkboxes[i];
            if (rule_checkbox.checked){
                data_to_send['rules_ids'].push(rule_checkbox.value);
                var flag = true;
            }
        }

        for (var i=0; i <rules_datepickers.length; i++){
            var datepicker = rules_datepickers[i];
            if (rules_checkboxes[i].checked){
                var date_arr = datepicker.value.split("/");
                var end_date = new Date(date_arr[2], date_arr[0] - 1, date_arr[1]);
                var duration = Math.round(Math.abs((end_date.getTime() - today.getTime())/(oneDay))) + 1;
                if (duration > 0) {
                    data_to_send['durations'].push(duration);
                }
                else {
                    alert("End date must be later than today (" + dd + "/" + mm + "/" + yyyy + "), please fix the end date/s");
                    return;
                }
            }
        }

        if (flag) {
        sendRequest(url, JSON.stringify(data_to_send), function (response) {

        });

        location.href = main_page;
        } else {
            alert("No rules selected, nothing to submit");
        }
    }

    function backButtonClick() {
       var main_page = "/ps/tools/apg_tool"
       location.href = main_page;
    }

    function initDataTable(selector, scrollX, height, scrollCollapse, bFilter, bInfo, paging, autoWidth){

        var initializer = {
            "order": [[2, "asc"]],
            "scrollX": scrollX,
            "scrollY": height,
            "scrollCollapse": scrollCollapse,
            "bFilter": bFilter,
            "bInfo": bInfo,
            "paging": paging,
            "autoWidth": autoWidth,
            "bSortable": true,
            "columnDefs": [{targets: "_all", className: "dt-center"}]
        };

        selector.DataTable(initializer);
    }

    submitButton.on("click", submitButtonClick);
    devicesSelect.on("change", dropdownSelect);
    backButton.on("click", backButtonClick);
    initDataTable(jobsTable, true, false, false, true, false, true, false);
    initDataTable(rulesTable, true, false, false, true, false, true, false);

    endDateSelector.datepicker();

})();
