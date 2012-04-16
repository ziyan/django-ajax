(($, exports) ->
  'use strict'

  call_function = (method, func, argv, callback) ->
    request = $.ajax
      type: method
      url: '/ajax/' + func + '/'
      dataType: 'json'
      data:
        argv: JSON.stringify(argv)
      beforeSend: (xhr) ->
        xhr.setRequestHeader "X-CSRFToken", $.cookie("csrftoken") if method is 'POST'

    request.done (data) ->
      if data and data._ajax_redirect

        if not $.pjax
          window.location.replace(data._ajax_redirect)
          return

        $.pjax
          url: data._ajax_redirect

        return

      if callback
        callback data, {}

    request.error (xhr, txt_status) ->
      return if not callback
      callback null,
        ajax_error: txt_status

  exports.get = (func, argv, callback) ->
    call_function 'GET', func, argv, callback

  exports.post = (func, argv, callback) ->
    call_function 'POST', func, argv, callback

)(jQuery, window)

