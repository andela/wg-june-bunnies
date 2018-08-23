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
      $('#compare_weight_diagrams').show();
    } else {
      $('#compare').hide();
      $('#compare_weight_diagrams').hide();
    }
  });
   $('#compare').click(function () {
    var users = [];
    var graph_data=[];
    var user_data;
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
            user_data = data
            graph_data.push(user_data);
          }else{
            error = username+" has no weight data to comapre";
          }  
        }
      });
     });  
      if (graph_data.length <=1){
        $('#compare_weight_diagrams').hide();
        $('#graph_error').html('<div class="alert alert-info">'+error+'</div>') 
      }else{
        // graph
        var myChart = new Chart(ctx, {
          type: 'line',
          data: {
            datasets: [{
                label: "user 1",
                data: graph_data[0],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            }]
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

