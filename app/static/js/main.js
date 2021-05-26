jQuery(function ($) {
  "use strict";
  $.each(["show", "hide"], function (i, ev) {
    var el = $.fn[ev];
    $.fn[ev] = function () {
      this.trigger(ev);
      return el.apply(this, arguments);
    };
  });

  var csrftoken = $("meta[name=csrf-token]").attr("content");

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  // Preloader
  $(window).on("load", function () {
    if ($("#preloader").length) {
      $("#preloader")
        .delay(100)
        .fadeOut("slow", function () {
          $(this).remove();
        });
    }
  });

  // Hero typed
  if ($(".typed").length) {
    var typed_strings = $(".typed").data("typed-items");
    typed_strings = typed_strings.split(",");
    new Typed(".typed", {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000,
    });
  }

  // Activate smooth scroll on page load with hash links in the url
  $(document).ready(function () {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top;
        $("html, body").animate(
          {
            scrollTop: scrollto,
          },
          1500,
          "easeInOutExpo"
        );
      }
    }
  });

  $(document).on("click", ".mobile-nav-toggle", function (e) {
    $("body").toggleClass("mobile-nav-active");
    $(".mobile-nav-toggle i").toggleClass(
      "icofont-navigation-menu icofont-close"
    );
  });

  $(document).click(function (e) {
    var container = $(".mobile-nav-toggle");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ($("body").hasClass("mobile-nav-active")) {
        $("body").removeClass("mobile-nav-active");
        $(".mobile-nav-toggle i").toggleClass(
          "icofont-navigation-menu icofont-close"
        );
      }
    }
  });

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $(".back-to-top").fadeIn("slow");
    } else {
      $(".back-to-top").fadeOut("slow");
    }
  });

  $(".back-to-top").click(function () {
    $("html, body").animate(
      {
        scrollTop: 0,
      },
      1500,
      "easeInOutExpo"
    );
    return false;
  });

  // jQuery counterUp
  $('[data-toggle="counter-up"]').counterUp({
    delay: 10,
    time: 1000,
  });

  // Skills section
  $(".progress .progress-bar").each(function () {
    $(this).css("width", $(this).attr("aria-valuenow") + "%");
  });

  // Init AOS
  function aos_init() {
    AOS.init({
      duration: 1000,
      once: true,
    });
  }

  // Porfolio isotope and filter
  $(window).on("load", function () {
    var portfolioIsotope = $(".portfolio-container").isotope({
      itemSelector: ".portfolio-item",
    });

    $("#portfolio-flters li").on("click", function () {
      $("#portfolio-flters li").removeClass("filter-active");
      $(this).addClass("filter-active");

      portfolioIsotope.isotope({
        filter: $(this).data("filter"),
      });
      aos_init();
    });

    // Initiate venobox (lightbox feature used in portofilo)
    $(".venobox").venobox({
      share: false,
    });

    // Initiate aos_init() function
    aos_init();

    $("body").tooltip({
      selector: '[data-toggle="tooltip"]',
      trigger: "hover",
    });
  });

  // Portfolio details carousel
  $(".portfolio-details-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    items: 1,
  });

  $(function () {
    $("#datepick").daterangepicker({
      timePicker: true,
      startDate: moment().startOf("hour"),
      endDate: moment().startOf("hour").add(32, "hour"),
      locale: {
        format: "M/DD hh:mm A",
      },
    });
  });

  $("#formModal").appendTo("body");
  $(function () {
    $("#msg").hide();

    $("#todo-form").hide();
    $("#cat-form").hide();
    $("#task-form").hide();
    $("#empl-form").hide();

    $("#create-btn").hide();
    $("#add-btn").hide();
    $("#edit-btn").hide();
    $("#delete-btn").hide();
    $("#update-btn").hide();

    $("#doneBlock").hide();
    $("#cat-list").hide();
    $("#empl-list").hide();
    $("#task-list").hide();

    //#region CREATE BTNS
    $("#create-task-form").on("click", function (event) {
      add_todo(1);
    });
    $("#create-cat-form").on("click", () => {
      add_todo(2);
    });
    $("#create-empl-form").on("click", () => {
      add_todo(3);
    });
    //#endregion
  });

  // Check if url contains some string for open modal form
  if (window.location.href.indexOf("&auth_req") > -1) {
    $("#userModal").modal("show");
    render_auth_modal();

    Swal.fire({
      title: "Authentication error!",
      text: "To access the page, first log in to your account.",
      icon: "warning",
      confirmButtonText: "Ok",
    });
  }
});

// #region TODO CRUD
function add_todo(type) {
  var ajax_url, $table, log;
  if (type === 1) {
    // TASK
    log = ["TASK", "TASKS"];
    $("#cat-form").hide();
    $("#empl-form").hide();
    $("#task-list").hide();
    $("#cat-list").hide();
    $("#empl-list").hide();

    $("#task-form").show();

    $("#todo-form").attr("action", "/todo/create");
    $("#formModalLabel").html("Add new Task");
  } else if (type === 2) {
    // CATEGORY
    log = ["CATEGORY", "CATEGORIES"];
    $table = $("#view-cat-table");
    ajax_url = "/todo/category/view";
    $("#empl-form").hide();
    $("#task-list").hide();
    $("#empl-list").hide();
    $("#task-form").hide();

    $("#cat-form").show();
    $("#cat-list").show();

    $("#todo-form").attr("action", "/todo/category/create");
    $("#formModalLabel").html("Add new Category");
  } else {
    // EMPLOYEE
    log = ["EMPLOYEE", "EMPLOYEES"];
    $table = $("#view-empl-table");
    ajax_url = "/todo/employee/view";
    $("#cat-form").hide();
    $("#task-list").hide();
    $("#cat-list").hide();
    $("#task-form").hide();
    $("#view-empl-table").bootstrapTable("hideColumn", "Title");
    $("#view-empl-table").bootstrapTable("hideColumn", "Category");
    $("#view-empl-table").bootstrapTable("hideColumn", "Priority");
    $("#view-empl-table").bootstrapTable("hideColumn", "Deadline");
    $("#view-empl-table").bootstrapTable("hideColumn", "Status");

    $("#empl-form").show();
    $("#empl-list").show();

    $("#view-empl-table").bootstrapTable("showColumn", "Id");
    $("#view-empl-table").bootstrapTable("showColumn", "Name");
    $("#view-empl-table").bootstrapTable("showColumn", "compl_tasks");
    $("#view-empl-table").bootstrapTable("showColumn", "todo_tasks");
    $("#view-empl-table tfoot").removeClass("thead-dark");

    $("#todo-form").attr("action", "/todo/employee/create");
    $("#formModalLabel").html("Add new Employee");
  }
  $("#todo-form").show();
  $("#msg").hide();
  $(".modal-dialog").removeClass("modal-xl");
  $("#todo-form").trigger("reset");

  $("#edit-btn").hide();
  $("#delete-btn").hide();
  $("#add-btn").hide();
  $("#update-btn").hide();

  dateRange();
  $("#closeModal").show();
  $("#create-btn").show();
  $("#create-btn").html("Add");

  if (type !== 1) {
    $.ajax({
      type: "GET",
      url: ajax_url,
      success: function (res) {
        var json = JSON.parse(res);
        $table.bootstrapTable("load", json);
      },
      error: function (error) {},
    });
  }

  $("#create-btn").off();
  $("#create-btn").on("click", function (event) {
    create_update_todo(log[1]);
    event.preventDefault();
  });
  $("#doneBlock").hide();
}
function create_update_todo(log) {
  var form = $("#todo-form");
  $.ajax({
    type: form.attr("method"),
    url: form.attr("action"),
    data: form.serialize(),
    success: function (response) {
      var json = JSON.parse(response);
      if (json.success == "true") {
        $("#formModal").modal("hide");
        $("#ToDos").html(json.data);
      } else {
        $("#msg")
          .show()
          .html(json.msg)
          .removeClass("alert-success")
          .addClass("alert-danger");
        for (const key in json.errors) {
          $("#" + key)
            .removeClass("is-valid")
            .addClass("is-invalid");
          $("#" + key + "-validation")
            .html(json.errors[key][0])
            .removeClass("valid-feedback")
            .addClass("invalid-feedback");
        }
        for (const key in json.data) {
          if (!json.errors.hasOwnProperty(key)) {
            $("#" + key)
              .removeClass("is-invalid")
              .addClass("is-valid");
            $("#" + key + "-validation")
              .html("Looks good!")
              .removeClass("invalid-feedback")
              .addClass("valid-feedback");
          }
        }
      }
    },
    error: function (error) {},
  });
}
function edit_todo(elm, type) {
  var ajax_url;
  if (type === 1) {
    // TASK
    ajax_url = `/todo/${elm}/get_by_id`;
    $("#cat-form").hide();
    $("#empl-form").hide();
    $("#task-list").hide();
    $("#cat-list").hide();
    $("#empl-list").hide();

    $("#task-form").show();
    $("#doneBlock").show();
    dateRange();

    $("#todo-form").attr("action", `/todo/${elm}/update`);
    $("#formModalLabel").html(`Edit Task-${elm}`);
  } else if (type === 2) {
    // CATEGORY
    ajax_url = `/todo/category/view`;
    $("#empl-form").hide();
    $("#task-list").hide();
    $("#empl-list").hide();
    $("#task-form").hide();

    $("#cat-form").show();
    $("#cat-list").show();

    $("#todo-form").attr("action", `/todo/category/${elm}/update`);
    $("#formModalLabel").html(`Edit Category '${elm}'`);
  } else {
    // EMPLOYEE
    ajax_url = `/todo/employee/view`;
    $("#cat-form").hide();
    $("#task-list").hide();
    $("#cat-list").hide();
    $("#task-form").hide();
    $("#view-empl-table").bootstrapTable("hideColumn", "Title");
    $("#view-empl-table").bootstrapTable("hideColumn", "Category");
    $("#view-empl-table").bootstrapTable("hideColumn", "Priority");
    $("#view-empl-table").bootstrapTable("hideColumn", "Deadline");
    $("#view-empl-table").bootstrapTable("hideColumn", "Status");
    $("#view-empl-table").bootstrapTable("showColumn", "Id");
    $("#view-empl-table").bootstrapTable("showColumn", "Name");
    $("#view-empl-table").bootstrapTable("showColumn", "compl_tasks");
    $("#view-empl-table").bootstrapTable("showColumn", "todo_tasks");
    $("#view-empl-table tfoot").removeClass("thead-dark");

    $("#empl-form").show();
    $("#empl-list").show();

    $("#todo-form").attr("action", `/todo/employee/${elm}/update`);
    $("#formModalLabel").html(`Edit Employee '${elm}'`);
  }
  $(".modal-dialog").removeClass("modal-xl");

  $("#edit-btn").hide();
  $("#create-btn").hide();
  $("#delete-btn").hide();
  $("#add-btn").hide();
  $("#update-btn").hide();

  $("#todo-form").show();
  $("#closeModal").show();
  $("#update-btn").show();

  $("#update-btn").off();
  $("#update-btn").on("click", function (event) {
    create_update_todo();
    event.preventDefault();
  });
  $.ajax({
    url: ajax_url,
    type: "GET",
    success: function (res) {
      var json = JSON.parse(res);
      if (type === 1) {
        $("#title").val(json.title);
        $("#priority").val(json.priority);
        $("#timeline").val(json.timeline);
        $("#category").val(json.category);
        for (const item of json.employee) {
          $("#employee")
            .find("option[value=" + item + "]")
            .prop("selected", "selected");
        }
        $("#description").val(json.description);
        $("#is_done").prop("checked", json.is_done);
      } else {
        var $table;
        if (type === 2) {
          $.ajax({
            type: "POST",
            url: `/todo/category/${elm}`,
            success: function (res) {
              var json = JSON.parse(res);
              for (const item of json) {
                $("#cat_tasks")
                  .find("option[value=" + item.Id + "]")
                  .prop("selected", "selected");
              }
            },
            error: function (error) {},
          });
          $("#cat_name").val(elm);

          if (elm === "Others") {
            $("#cat_name").attr("readonly", true);
          } else {
            $("#cat_name").attr("readonly", false);
          }
          $table = $("#view-cat-table");
        } else {
          $.ajax({
            type: "POST",
            url: `/todo/employee/${elm}`,
            success: function (res) {
              var json = JSON.parse(res);
              for (const item of json) {
                $("#empl_tasks")
                  .find("option[value=" + item.Id + "]")
                  .prop("selected", "selected");
              }
            },
            error: function (error) {},
          });
          if (elm === "Maksym") {
            $("#empl_name").attr("readonly", true);
          } else {
            $("#empl_name").attr("readonly", false);
          }
          $("#empl_name").val(elm);
          $table = $("#view-empl-table");
        }
        $table.bootstrapTable("load", json);
      }
    },
    error: function (error) {},
  });
}
function delete_todo(elm, type) {
  var ajax_url, log;
  if (type === 1) {
    log = "TASK";
    ajax_url = `/todo/${elm}/delete`;
  } else if (type === 2) {
    log = "CATEGORY";
    ajax_url = `/todo/category/${elm}/delete`;
  } else {
    log = "EMPLOYEE";
    ajax_url = `/todo/employee/${elm}/delete`;
  }
  $.ajax({
    type: "POST",
    url: ajax_url,
    success: function (res) {
      var json = JSON.parse(res);
      if (json.success == "true") {
        $("#formModal").modal("hide");
        $("#ToDos").html(json.data);
      } else {
        alert(json.msg);
      }
    },
    error: function (error) {},
  });
}
function done_change(elm) {
  elm = Number(elm);
  $.ajax({
    type: "POST",
    url: `/todo/${elm}/mark_todo`,
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({
      check: $(`#check-${elm}`).prop("checked"),
    }),
    success: function (res) {
      $("#ToDos").html(res.data);
    },
    error: function (error) {},
  });
}
function view_todo(elm, type) {
  var $table, ajax_url, log;
  if (type === 1) {
    // TASK
    log = "Task";
    $table = $("#view-task-table");
    ajax_url = `/todo/${elm}`;
    $("#task-form").hide();
    $("#todo-form").hide();
    $("#cat-form").hide();
    $("#empl-form").hide();
    $("#cat-list").hide();
    $("#empl-list").hide();

    $("#task-list").show();

    $("#view-task-table").bootstrapTable("showColumn", "Category");
  } else if (type === 2) {
    // CATEGORY
    log = "Category";
    $table = $("#view-task-table");
    ajax_url = `/todo/category/${elm}`;
    ajax_url_permission = `/todo/category/${elm}/permission`;
    $("#todo-form").hide();
    $("#task-form").hide();
    $("#empl-form").hide();
    $("#empl-list").hide();
    $("#cat-form").hide();
    $("#cat-list").hide();

    $("#task-list").show();

    $("#view-task-table").bootstrapTable("hideColumn", "Category");
  } else {
    // EMPLOYEE
    log = "Employee";
    $table = $("#view-empl-table");
    ajax_url = `/todo/employee/${elm}`;
    ajax_url_permission = `/todo/employee/${elm}/permission`;
    $("#todo-form").hide();
    $("#task-form").hide();
    $("#task-list").hide();
    $("#cat-form").hide();
    $("#cat-list").hide();
    $("#empl-form").hide();
    $("#view-empl-table").bootstrapTable("hideColumn", "Id");
    $("#view-empl-table").bootstrapTable("hideColumn", "Name");
    $("#view-empl-table").bootstrapTable("hideColumn", "compl_tasks");
    $("#view-empl-table").bootstrapTable("hideColumn", "todo_tasks");

    $("#empl-list").show();

    $("#view-empl-table").bootstrapTable("showColumn", "Title");
    $("#view-empl-table").bootstrapTable("showColumn", "Category");
    $("#view-empl-table").bootstrapTable("showColumn", "Priority");
    $("#view-empl-table").bootstrapTable("showColumn", "Deadline");
    $("#view-empl-table").bootstrapTable("showColumn", "Status");

    $("#view-empl-table tfoot").removeClass("thead-dark");
    $("#view-empl-table tfoot").addClass("thead-dark");
  }

  $("#closeModal").hide();
  $("#create-btn").hide();
  $("#update-btn").hide();

  $("#add-btn").show();
  $("#edit-btn").show();
  $("#delete-btn").show();
  if (type !== 3) {
    $(".modal-dialog").removeClass("modal-xl");
    $(".modal-dialog").addClass("modal-xl");
  } else {
    $(".modal-dialog").removeClass("modal-xl");
  }

  $("#delete-btn").off();
  $("#edit-btn").off();
  $("#add-btn").off();

  $("#delete-btn").on("click", () => {
    delete_todo(elm, type);
  });
  $("#edit-btn").on("click", () => {
    edit_todo(elm, type);
  });
  $("#add-btn").on("click", () => {
    add_todo(type);
  });
  $.ajax({
    type: "POST",
    url: ajax_url,
    success: function (res) {
      var json = JSON.parse(res);
      if (type === 1) {
        $("#formModalLabel").html(`${log} <b>${json.Title}</b>`);
      } else {
        $("#formModalLabel").html(`${log} <b>${elm}</b>`);
      }
      if (type === 3) {
        if (json.length !== 0) {
          window.doneLabel = "Completed Tasks";
          window.doneValue = json[0].compl_tasks;
          window.todoLabel = "Todo Tasks";
          window.todoValue = json[0].todo_tasks;
        }
      }
      $table.bootstrapTable("removeAll");
      $table.bootstrapTable("append", json);
    },
    error: function (error) {},
  });
}
// #endregion
var doneLabel, doneValue, todoLabel, todoValue;
function dateRange() {
  var start = moment();
  var end = moment().endOf("day");

  function setInput(start, end) {
    $("#timeline").val(
      start.format("MMM-D HH:mm") + " - " + end.format("MMM-D HH:mm")
    );
  }

  $("#date-range-open").daterangepicker(
    {
      timePicker: true,
      timePicker24Hour: true,
      startDate: start,
      endDate: end,
      ranges: {
        Today: [moment(), moment().endOf("day")],
        Tomorrow: [moment(), moment().add(1, "d").endOf("day")],
        "This week": [moment(), moment().endOf("week")],
        "This mounth": [moment(), moment().endOf("month")],
      },
    },
    setInput
  );

  setInput(start, end);
}

function done_label() {
  return doneLabel;
}
function done_value() {
  return doneValue;
}
function todo_label() {
  return todoLabel;
}
function todo_value() {
  return todoValue;
}

// #region USER
$("#user-list").bootstrapTable({
  classes: "table table-hover table-striped",

  pagination: true,
  striped: true,
  sortable: true,
  pageSize: 8,
  pageList: [8, 10, 25, 50, 100],
});

function render_auth_modal() {
  $.ajax({
    type: "GET",
    url: "/user_form",
    success: function (response) {
      var json = JSON.parse(response);

      if (json.success == "AUTH") {
        $("#userModal").modal("hide");
      } else {
        $("#userModal").html(json.data);
      }
    },
    complete: function () {
      const sign_in_btn = document.querySelector("#sign-in-btn");
      const sign_up_btn = document.querySelector("#sign-up-btn");
      const container = document.querySelector(".user-container");

      const submit_up = document.getElementById("sign-up-submit");
      const submit_in = document.getElementById("sign-in-submit");

      submit_up.addEventListener("click", function (event) {
        user_request(1);
        event.preventDefault();
      });

      submit_in.addEventListener("click", function (event) {
        user_request(2);
        event.preventDefault();
      });

      sign_up_btn.addEventListener("click", () => {
        container.classList.remove("sign-in-mode");
        $(".sign-up-form").trigger("reset");
        $(".sign-up-form .input-field").css("border", "");
        $(".sign-up-form .u_times").css("display", "none");
        $(".sign-up-form .u_check").css("display", "none");
        $(".sign-up-form .input-field span").css("color", "");
      });

      sign_in_btn.addEventListener("click", () => {
        container.classList.add("sign-in-mode");
        $(".sign-in-form").trigger("reset");
        $(".sign-in-form .input-field").css("border", "");
        $(".sign-in-form .input-field span").css("color", "");
        $(".sign-in-form .u_times").css("display", "none");
        $(".sign-in-form .u_check").css("display", "none");
      });

      if (window.location.href.indexOf("&auth_req") > -1) {
        sign_in_btn.click();
      }
    },
  });
}

function user_request(type, user_id) {
  // 1 ===> Sign up
  // 2 ===> Sign in
  // 3 ===> Update info
  // 4 ===> Change password
  // 5 ===> Admin Create User
  // 6 ===> Admin Update User
  var ajax_url, $form, form, msg;
  if (Number(type) === 1) {
    ajax_url = "/signup";
    form = ".sign-up-form";
    msg = "registered.";
  } else if (Number(type) === 2) {
    ajax_url = "/signin";
    form = ".sign-in-form";
    msg = "logged in.";
  } else if (Number(type) === 3) {
    ajax_url = `/user/${user_id}/edit`;
    form = ".user-edit-form";
    msg = "updated.";
  } else if (Number(type) === 4) {
    ajax_url = `/user/${user_id}/password/change`;
    form = ".user-edit-form";
    msg = "changed password.";
  } else if (Number(type) === 5) {
    ajax_url = `/admin/create/user`;
    form = ".user-edit-form";
    msg = "created new User.";
  } else {
    ajax_url = `/admin/update/user/${user_id}`;
    form = ".user-edit-form";
    msg = "created new User.";
  }
  var data_request = new FormData(document.querySelector(form));

  $.ajax({
    type: $(form).attr("method"),
    url: ajax_url,
    data: data_request,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      var json = JSON.parse(response);
      if (json.success == "OK") {
        $(form).trigger("reset");

        $(`${form} .input-field`).css("border", "");
        $(`${form} textarea`).css("border", "");
        $(`${form} .input-field span`).css("color", "");
        $(`${form} .u_times`).css("display", "none");
        $(`${form} .u_check`).css("display", "none");

        if (Number(type) === 2) {
          $("#header").html(json.data);
        }
        if (Number(type) === 5 || Number(type) === 6) {
          $("#user-list").bootstrapTable("load", json.data);
          Swal.fire({
            title: "You successfully " + msg,
            icon: "success",
            confirmButtonText: "Ok",
          }).then(() => {
            $("#userEditModal").modal("hide");
          });
        } else {
          Swal.fire({
            title: "You successfully " + msg,
            icon: "success",
            confirmButtonText: "Ok",
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.pathname = "/account";
            }
          });
        }
      } else {
        Swal.fire({
          title: "There are some errors during validation!",
          icon: "error",
          confirmButtonText: "Ok",
        });
        for (const key in json.data) {
          if (!json.errors.hasOwnProperty(key)) {
            $("#" + key)
              .closest(".input-field")
              .css("border", "1px solid green");
            if (Number(type) === 3) {
              $("textarea#" + key).css("border", "2px solid green");
            }
            $("#" + key)
              .siblings("span")
              .css("color", "green");
            $("#" + key)
              .siblings(".u_times")
              .css("display", "none");
            $("#" + key)
              .siblings(".u_check")
              .css("display", "block")
              .tooltip({
                placement: "left",
                title: "Looks good!",
              });
          }
        }
        for (const key in json.errors) {
          $("#" + key)
            .closest(".input-field")
            .css("border", "1px solid red");
          if (Number(type) === 3) {
            $("textarea#description").css("border", "2px solid red");
          }
          $("#" + key)
            .siblings("span")
            .css("color", "red");
          $("#" + key)
            .siblings(".u_times")
            .css("display", "block")
            .tooltip({
              placement: "left",
              title: "",
            })
            .attr("title", json.errors[key][0])
            .tooltip("_fixTitle");
          $("#" + key)
            .siblings(".u_check")
            .css("display", "none");
        }
      }
    },
  });
}

function user_info_edit(user_id) {
  $.ajax({
    type: "GET",
    url: `/user/${user_id}/get`,
    success: function (response) {
      var json = JSON.parse(response);
      $("#userEditModal").html(json.data);
      $("#username").val(json.name);
      $("#email").val(json.email);
      $("#description").val(json.description);
    },
    complete: function () {
      $("#userEditModal .title").html("Update user info");
      $("#user-edit-submit").html("Update");

      $(".change__pass-label").show();
      $(".edit__info").show();
      $(".change__pass").hide();

      const submit_edit = document.getElementById("user-edit-submit");

      submit_edit.replaceWith(submit_edit.cloneNode(true));
      $("#user-edit-submit").on("click", function (event) {
        user_request(3, user_id);
        event.preventDefault();
      });
    },
  });
}

function admin_create() {
  $.ajax({
    type: "GET",
    url: `/admin/render-forms`,
    success: function (response) {
      var json = JSON.parse(response);
      $("#userEditModal").html(json.data);
    },
    complete: function () {
      $("#userEditModal .title").html("Create new User");
      $("#user-edit-submit").html("Create");

      $(".admin-create-form").show();
      $(".admin-update-form").hide();

      const submit_edit = document.getElementById("user-edit-submit");

      submit_edit.replaceWith(submit_edit.cloneNode(true));
      $("#user-edit-submit").on("click", function (event) {
        user_request(5);
        event.preventDefault();
      });
    },
  });
}

function admin_update(user_id) {
  $.ajax({
    type: "GET",
    url: `/admin/user/${user_id}/get`,
    success: function (response) {
      var json = JSON.parse(response);
      $("#userEditModal").html(json.data);
      $("#username_admin_update").val(json.name);
      $("#email_admin_update").val(json.email);
      $("#is_admin_update").prop("checked", json.admin);
    },
    complete: function () {
      $("#userEditModal .title").html("Update User data");
      $("#user-edit-submit").html("Update");

      $(".admin-create-form").hide();
      $(".admin-update-form").show();

      const submit_edit = document.getElementById("user-edit-submit");

      submit_edit.replaceWith(submit_edit.cloneNode(true));
      $("#user-edit-submit").on("click", function (event) {
        user_request(6, user_id);
        event.preventDefault();
      });
    },
  });
}

function admin_delete(user_id) {
  $.ajax({
    url: `/admin/delete/user/${user_id}`,
    success: function (response) {
      var json = JSON.parse(response);
      if (json.success == "OK") {
        $("#user-list").bootstrapTable("load", json.data);
        Swal.fire({
          title: "Operation completed!",
          text: "User have been deleted successfully.",
          icon: "success",
          confirmButtonText: "Ok",
        });
      }
    },
  });
}

function change_pass_form(user_id) {
  const submit_pass = document.getElementById("user-edit-submit");

  $("#userEditModal .title").html("Change user password");
  $("#user-edit-submit").html("Change");

  $(".change__pass-label").hide();
  $(".edit__info").hide();
  $(".change__pass").show();

  submit_pass.replaceWith(submit_pass.cloneNode(true));

  $("#user-edit-submit").on("click", function (event) {
    user_request(4, user_id);
    event.preventDefault();
  });
}

function admin_view(user_id) {
  $.ajax({
    type: "GET",
    url: `/admin/view/user/${user_id}`,
    success: function (response) {
      var json = JSON.parse(response);
      $(".user__title h3").html(json.username);
      $(".user__email h4").html(json.email);
      $(".user__visit p").html("Last seen " + json.last_seen);
      $(".user__description p").html(
        json.description
          ? json.description
          : "Please, tell us somemething about you &#128521;"
      );
      $(".profile__img")[0].style.backgroundImage = `url(${json.image})`;

      if (json.id === 1) {
        $(".profile__img span").show();
      } else {
        $(".profile__img span").hide();
      }
      document.querySelector("#choice1").checked = false;
    },
  });
}

function logout() {
  Swal.fire({
    title: "You successfully logout.",
    icon: "success",
    confirmButtonText: "Ok",
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.pathname = "/logout";
    }
  });
}
// #endregion

// #region ADMIN ACCOUNT ANIMATIONS
if (window.location.href.indexOf("/account") > -1) {
  const st = {};

  st.flap = document.querySelector("#flap");
  st.toggle = document.querySelector("#user .toggle");

  st.choice1 = document.querySelector("#choice1");
  st.choice2 = document.querySelector("#choice2");

  st.table = document.querySelector("#user .user-list");
  st.user_info = document.querySelector("#user .profile");

  st.switch_panel = document.querySelector("#switch-panel");

  st.flap.addEventListener("transitionend", () => {
    if (st.choice1.checked) {
      st.toggle.style.transform = "rotateY(-15deg)";
      st.switch_panel.style.transform = "perspective(120vw) rotateY(-180deg)";
      setTimeout(() => (st.toggle.style.transform = ""), 400);
    } else {
      st.toggle.style.transform = "rotateY(15deg)";
      st.switch_panel.style.transform = "perspective(120vw) rotateY(0deg)";
      setTimeout(() => (st.toggle.style.transform = ""), 400);
    }
  });

  st.clickHandler = (e) => {
    if (e.target.tagName === "LABEL") {
      setTimeout(() => {
        st.flap.children[0].textContent = e.target.textContent;
      }, 250);
    }
  };

  document.addEventListener("DOMContentLoaded", () => {
    st.flap.children[0].textContent = st.choice2.nextElementSibling.textContent;
  });

  document.addEventListener("click", (e) => st.clickHandler(e));
}

function access_denied() {
  Swal.fire({
    title: "Access denied!",
    text: "You don't have permission for this operation.",
    icon: "warning",
    confirmButtonText: "Ok",
  });
}
// #endregion
