/*
 This file is part of wger Workout Manager.
  wger Workout Manager is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
  wger Workout Manager is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
  You should have received a copy of the GNU Affero General Public License
 */
'use strict';
 $(document).ready(function () {
  $('#compare').hide();
  $('#compare_weight_diagrams').hide();
  var url;
  var username;
  var nametext;
  var checkboxes;
  
   $('input[type=checkbox].checkbox').change(function () {
    checkboxes = $('input[type=checkbox].checkbox:checked');
    if (checkboxes.size() === 2) {
      $('#compare').show();
    } else {
      $('#compare').hide();
      $('#compare_weight_diagrams').hide();
      $('#compare_weight_diagrams').html('');
      $('#graph_error').html('');
      
    }
  });
   $('#compare').click(function () {
    var users = [];
    var graph_data=[];
    var test_data= [];
    var user_data={"user":'',"data":''};
    var error;
    var ctx = $('#compare_weight_diagrams')
    // loop through selected users 
    $(checkboxes).each(function (index) {
      username = $(this).attr('id');
      nametext = $(this).attr('value');
      url = '/weight/api/compare_weight_data/' + username;
      users.push(nametext + ' (' + username + ')');
      // get data to compare
      $.ajax({
        async: false,
        type: 'GET',
        url: url,
        success: function(data) {
          if (data.length > 0) {
            graph_data.push({'user':username, 'data': data});
          }else{
            error = '<b>'+username+'</b>'+" has no weight data to comapre";
          }  
        }
      });
     });  
      if (graph_data.length <=1){
        $('#compare_weight_diagrams').hide();
        $('#graph_error').html('<div class="alert alert-info">'+error+'</div>') 
      }else{
        console.log(graph_data[0].data)
        $('#compare_weight_diagrams').show();
        var labels=[];
        if(graph_data[0].data.length > graph_data[1].data.length){
          for (var l=0; l<graph_data[0].data.length; l++){labels.push(graph_data[0].data[l].x)}
        }else{
          for (var l=0; l<graph_data[1].data.length; l++){labels.push(graph_data[1].data[l].x)}
        }
        var myChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
                label: graph_data[0].user,
                data: graph_data[0].data,
                borderColor: [
                    'rgba(255,99,132,1)'
                ],
                borderWidth: 2
            },
            {
              label: graph_data[1].user,
              data: graph_data[1].data,
              type: 'line',
              borderColor: [
                'rgba(0,0,255,1)'
            ],
            borderWidth: 2
            }
          ]
          },
          options: {
              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero:true
                      }
                  }]
              }
          }
        });
        // EOF graph
      }
  });
});

