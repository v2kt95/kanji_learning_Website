/*
 *
 *   Vuongdv3 kanji learning
 *   version 1.0
 *
 */
$(document).ready(function(){

  $("#next").click(function(){
    $("#mark").removeClass("btn-danger").addClass("btn-warning");
    get_word().then(function(res) {
      if (res.is_empty == false) {
        $("#kanji_meaning").val(res.kanji_meaning)
        $("#kanji").val(res.kanji)
        $("#hiragana_form").val(res.hiragana_form)
        $("#kanji_form").val(res.kanji_form)
        $("#meaning_form").val(res.meaning_form)
        $("#main_label").html(res.hiragana_form);
      }
      else{
        $("#main_label").html("終わりましょ");
      }        
    }).catch(function(err){
        console.log(err);
    });

    get_done_word().then(function(res) {
        update_done_table(res.result)
    }).catch(function(err){
        console.log(err);
    });

    get_remain_word().then(function(res) {
        update_remain_table(res.result)      
    }).catch(function(err){
        console.log(err);
    });

  });

  $("#show").click(function(){
    switch($("#main_label").html()) {
      case $("#hiragana_form").val():
        $("#main_label").html($("#kanji_form").val());
        break;
      case $("#kanji_form").val():
        $("#main_label").html($("#meaning_form").val());
        break;
      default:
        $("#main_label").html($("#hiragana_form").val());
    }
  });

  $("#reset").click(function(){
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'reset',
        success: function(data) {
            deferred.resolve(data);
        },
        error: function(err) {
            console.log(err);
            deferred.reject(err);
        }
    });
  });

  $("#mark").click(function(){
    $("#mark").removeClass("btn-warning").addClass("btn-danger");
    var hiragana_mark = $("#hiragana_form").val();
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'mark_word?word='+hiragana_mark,
        success: function(data) {
            deferred.resolve(data);
        },
        error: function(err) {
            console.log(err);
            deferred.reject(err);
        }
    });
  });

});


function update_done_table(done_list)
{
    var html = "";
    for (var i = 0; i < done_list.length; i++) {
        html += '<tr>';
        html += '<td>' + (i + 1) + '</td>';
        html += '<td>' + done_list[i].kanji_form + '</td>';
        html += '</tr>';
    }
    $('#done_table tbody').html(html);
}

function update_remain_table(remain_list)
{
    var html = "";
    for (var i = 0; i < remain_list.length; i++) {
        html += '<tr>';
        html += '<td>' + (i + 1) + '</td>';
        html += '<td>' + remain_list[i].kanji_form + '</td>';
        html += '</tr>';
    }
    $('#remain_table tbody').html(html);
}

function get_word() {
    priority = $('#priority').is(":checked")
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'get_word?priority='+priority,
        success: function(data) {
            deferred.resolve(data);
        },
        error: function(err) {
            console.log(err);
            deferred.reject(err);
        }
    });
    return deferred.promise();
}

function get_done_word() {
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'get_list_done_word',
        success: function(data) {
            deferred.resolve(data);
        },
        error: function(err) {
            console.log(err);
            deferred.reject(err);
        }
    });
    return deferred.promise();
}

function get_remain_word() {
    priority = $('#priority').is(":checked")
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'get_list_remain_word?priority='+priority,
        success: function(data) {
            deferred.resolve(data);
        },
        error: function(err) {
            console.log(err);
            deferred.reject(err);
        }
    });
    return deferred.promise();
}