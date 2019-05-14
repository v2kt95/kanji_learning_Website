/*
 *
 *   Vuongdv3 kanji learning
 *   version 1.0
 *
 */

$(document).ready(function(){
  $('.slick_demo_1').slick({
        dots: true
    });

  update_bar_chart();    

  update_main_label("始めましょ");
  $("#next").click(function(){
    $("#mark").removeClass("btn-danger").addClass("btn-warning");
    get_word().then(function(res) {
      if (res.is_empty == false) {
        $("#kanji_meaning").val(res.kanji.kanji_meaning);
        $("#kanji").val(res.kanji.kanji);
        hiragana_form_list = [];
        kanji_form_list = [];
        meaning_form_list = [];
        res.word.forEach(function(element) {
          hiragana_form_list.push(element.hiragana_form);
          kanji_form_list.push(element.kanji_form);
          meaning_form_list.push(element.meaning_form);
        });

        $("#hiragana_form").val(hiragana_form_list.join(","));
        $("#kanji_form").val(kanji_form_list.join(","));
        $("#meaning_form").val(meaning_form_list.join(","));
        update_main_label(hiragana_form_list.join(","));
        $("#current_state").val("hiragana_form"); //current state : hiragana_form, kanji_form, meaning_form
      }
      else{        
        update_main_label("終わりましょ");
        alert(res.alert)
      }        
    }).catch(function(err){
        console.log(err);
    });

    get_done_word().then(function(res) {
        update_done_table(res.result);
    }).catch(function(err){
        console.log(err);
    });

    get_remain_word().then(function(res) {
        update_remain_table(res.result);      
    }).catch(function(err){
        console.log(err);
    });

    update_bar_chart();

  });

  $("#show").click(function(){
    switch($("#current_state").val()) {
      case "hiragana_form":
        index_slide = $('.slick-active').data("slick-index");
        update_main_label($("#kanji_form").val());        
        $("#current_state").val("kanji_form");
        $('.slick_demo_1').slick('slickGoTo', index_slide);
        break;
      case "kanji_form":
        index_slide = $('.slick-active').data("slick-index");        
        update_main_label($("#meaning_form").val());
        $("#current_state").val("meaning_form");
        $('.slick_demo_1').slick('slickGoTo', index_slide);
        break;
      default:
        index_slide = $('.slick-active').data("slick-index");
        update_main_label($("#hiragana_form").val());
        $("#current_state").val("hiragana_form");
        $('.slick_demo_1').slick('slickGoTo', index_slide);
    }
  });

  $("#reset").click(function(){
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'reset',
        success: function(data) {
            location.reload();
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
    var kanji_mark = $("#kanji").val();
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'mark_word?word='+kanji_mark,
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
        html += '<td>' + done_list[i].kanji + '</td>';
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
        html += '<td>' + remain_list[i].kanji + '</td>';
        html += '</tr>';
    }
    $('#remain_table tbody').html(html);
}

function get_word() {
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'get_word2',
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

function get_statistic_data() {
    var deferred = new $.Deferred();
    $.ajax({
        type: 'GET',
        url: 'get_statistic_kanji',
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

function update_main_label(string_value) {
    $('.main_label_element').remove();
    list_value = string_value.split(",");    
    list_value.forEach(function(element) {
      $('.slick_demo_1').prepend("<label class='main_label_element'>"+ element + "</label>");
    });
    $('.slick_demo_1').slick('removeSlide', null, null, true);
    $('.slick_demo_1').slick("unslick");
    $('.slick_demo_1').slick({
        dots: true
    });
}

function update_bar_chart() {
    get_statistic_data().then(function(res){
    let col = res.result.reduce((acc, daydown_data, index, daydown_datas) => {
        display_index = index+1;
        return acc.concat([["day down "+display_index].concat(daydown_data)]);
    }, [])
    c3.generate({
        bindto: '#stocked',
        data:{
            columns: col,
            // colors:{
            //     data1: '#1ab394',
            //     data2: '#BABABA',
            //     data3: '#212b3d',
            //     data4: '#ba1a52',
            // },
            type: 'bar',
            groups: [
                ['day down 1', 'day down 2', 'day down 3', 'day down 4']
            ]
        },
        axis: {
            x: {
                type: 'category',
                categories: ['lv1', 'lv2', 'lv3', 'lv4', 'lv5']
            }
        }
    });
  }).catch(function(err){
        console.log(err);
  });
}