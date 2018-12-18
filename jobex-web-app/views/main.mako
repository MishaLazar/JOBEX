<html>
<head>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <%include file="head.mako" args="title='JOBEX'"/>
    <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
    ${header()}
    ${nav()}
    %if function == 'main_page':
        ${main_page_renderer()}
    %elif function == 'job':
        ${job_renderer()}
    %elif function == 'process':
        ${process_renderer()}
    %endif
<script src="/static/css/bootstrap.min.css"></script>
<script src="/static/js/main.js"></script>
</body>
</html>

<%def name="header()">
    <header class="with-nav">
        <div class="custom-container row">
            <div class="three columns">
                <img class="logo" src="C:\JOBEX\jobex-web-app\static\images\jobex-logo.png" alt="jobex logo">
            </div>
            <div class="nine columns u-pull-right">
                <form class="u-pull-right" method="post" action="/.../logout"
                      onsubmit="sessionStorage.clear();">
                    <input id="logout-button" class="u-pull-right" type="submit" value="Logout"/>
                </form>
                <div class="u-pull-right" id="welcome-login">
                    %if username:
                        <p>Welcome, ${username}</p>
                    %endif
                </div>
            </div>
        </div>
    </header>
</%def>

<%def name="nav()">
    <nav class="navigation">
        <div class="custom-container row" id="nav-color">
            <h5>JOBEX</h5>
        </div>
    </nav>
</%def>

<%def name="main_page_renderer()">
    <div class="container box" id="container">
        <div class="container-fluid">
            %if error:
                <span class="u-pull-right" id="status">
                    ${error}
                </span>
            %else:
                <div class="row">

                </div>
                <div class="row">
                    <button type="button" class="btn btn-default" id="create_button" hidden="true">
                        Create Job/s
                    </button>
                </div>
                <div id="jobs_div">
                    <table class="display" id="jobs_table" cellspacing="0">
                        <thead>
                        <th>Job Name</th>
                        <th>Job Owner</th>
                        <th>Device</th>
                        <th>Started</th>
                        <th>End Date</th>
                        <th>Comment</th>
                        </thead>
                        <tbody>
                            %for job in jobs:
                                <tr>
                                    <td>${job.task_name}</td>
                                    <td>${job.user}</td>
                                    <td>${job.device}</td>
                                    <td>${job.insertion_date}</td>
                                    <td>${job.end_date}</td>
                                    <td>${job.comment}</td>
                                </tr>
                            %endfor
                        </tbody>
                    </table>
                </div>
                <div id="process_div">
                    <table class="display" id="jobs_table" cellspacing="0">
                        <thead>
                        <th>Process Name</th>
                        <th>Job Owner</th>
                        <th>Device</th>
                        <th>Started</th>
                        <th>End Date</th>
                        <th>Comment</th>
                        </thead>
                        <tbody>
                            %for job in jobs:
                                <tr>
                                    <td>${job.task_name}</td>
                                    <td>${job.user}</td>
                                    <td>${job.device}</td>
                                    <td>${job.insertion_date}</td>
                                    <td>${job.end_date}</td>
                                    <td>${job.comment}</td>
                                </tr>
                            %endfor
                        </tbody>
                    </table>
                </div>
            %endif
        </div>
    </div>
</%def>


<%def name="rules_renderer()">
    <div class="container box" id="container">
        <div class="container-fluid">
            %if error:
                <span class="u-pull-right" id="status">
                    ${error}
                </span>
            %else:
                <div id="rules_div">
                    <table class="display" id="rules_table" cellspacing="0">
                        <thead>
                        <th>Select</th>
                        <th>Permissiveness Level</th>
                        <th>Name</th>
                        <th>Source</th>
                        <th>Destination</th>
                        <th>VPN</th>
                        <th>Service</th>
                        <th>Action</th>
                        <th>Track</th>
                        <th>Install On</th>
                        <th>Comment</th>
                        <th>End Date</th>
                        </thead>
                        <tbody>
                            %for rule in rules:
                                <tr>
                                    <td><input type="checkbox" value="${rule.id}" class="rule_checkbox"/>&nbsp;</td>
                                    <td>${rule.documentation.permissiveness_level}</td>
                                    <td>${rule.name}</td>
                                    <td>
                                        %for network in rule.src_networks:
                                            ${network.display_name}
                                        %endfor
                                    </td>
                                    <td>
                                        %for network in rule.dst_networks:
                                            ${network.display_name}
                                        %endfor
                                    </td>
                                    <td>
                                        %for vpn in rule.vpn:
                                            ${vpn.display_name}
                                        %endfor
                                    </td>
                                    <td>
                                        %for service in rule.dst_services:
                                            ${service.display_name}
                                        %endfor
                                    </td>
                                    <td>${rule.action}</td>
                                    <td>${rule.track.level}</td>
                                    <td>${rule.install.display_name}</td>
                                    <td>${rule.comment}</td>
                                    <td><input class="datepicker" type="text"
                                               name="end-date"
                                               required="required"></td>
                                </tr>
                            %endfor
                        </tbody>
                    </table>
                </div>
                <div class="row">
                    <button type="button" class="btn btn-outline-dark" id="submit_button">
                        Submit
                    </button>
                    <button type="button" class="btn btn-outline-dark" id="back_button">
                        Back
                    </button>

                </div>
            %endif
        </div>
    </div>
</%def>