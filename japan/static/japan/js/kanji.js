/*
 *
 *   Vuongdv3 kanji learning
 *   version 1.0
 *
 */
$(document).ready(function(){

  $("#next").click(function(){
    get_word().then(function(res) {
      if (res.is_empty == false) {
        $("#kanji_meaning").val(res.kanji_meaning)
        $("#kanji").val(res.kanji)
        $("#hiragana_form").val(res.hiragana_form)
        $("#kanji_form").val(res.kanji_form)
        $("#meaning_form").val(res.meaning_form)
        $("#main_label").html(res.hiragana_form);
      }        
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


function update_mark_table(mark_list)
{
	var html = "";
	for (var i = 0; i < mark_list.length; i++) {
		html += '<tr>';
		html += '<td>' + (i + 1) + '</td>';
		html += '<td>' + mark_list[i] + '</td>';
		html += '</tr>';
	}
	$('#mark_table tbody').html(html);
}

function update_retain_table(hiragana_list)
{
	var html = "";
	for (var i = 0; i < hiragana_list.length; i++) {
		html += '<tr>';
		html += '<td>' + (i + 1) + '</td>';
		html += '<td>' + hiragana_list[i] + '</td>';
		html += '</tr>';
	}
	$('#retain_table tbody').html(html);
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