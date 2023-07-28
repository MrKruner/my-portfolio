let projects = document.getElementsByClassName('each_project');
let not_started = document.getElementById('not_started');
let planning = document.getElementById('planning');
let execute = document.getElementById('execute');
let completed = document.getElementById('completed');
let Delete = document.getElementById('delete');


function updateProjectProcess(project_id, process) {
  fetch('/update_project_process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id: project_id, process: process }),
  });
}

function deleteProject(project_id){
  fetch('/delete_project', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id: project_id}),
  });
}

for (let project of projects) {
    project.addEventListener('dragstart', function(e) {
    let selected = e.target;


    not_started.addEventListener('dragover', function(e) {
      e.preventDefault();
    });

    not_started.addEventListener('drop', function(e) {
      e.preventDefault();
      not_started.appendChild(selected);
      updateProjectProcess(selected.getAttribute('data-project-id'), 'not_started');
      selected = null;
    });


    planning.addEventListener('dragover', function(e) {
        e.preventDefault();
      });
  
    planning.addEventListener('drop', function(e) {
        e.preventDefault();
        planning.appendChild(selected);
        updateProjectProcess(selected.getAttribute('data-project-id'), 'planning');
        selected = null;
    });


    execute.addEventListener('dragover', function(e) {
        e.preventDefault();
      });
  
    execute.addEventListener('drop', function(e) {
        e.preventDefault();
        execute.appendChild(selected);
        updateProjectProcess(selected.getAttribute('data-project-id'), 'execute');
        selected = null;
    });


    completed.addEventListener('dragover', function(e) {
        e.preventDefault();
      });
  
    completed.addEventListener('drop', function(e) {
        e.preventDefault();
        completed.appendChild(selected);
        updateProjectProcess(selected.getAttribute('data-project-id'), 'completed');
        selected = null;
    });


    Delete.addEventListener('dragover', function(e){
      e.preventDefault();
    });

    Delete.addEventListener('drop', function(){
      deleteProject(selected.getAttribute('data-project-id'));
      location.reload();
    });

  });
}


