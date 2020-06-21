var initialize = function(navigator, user, token, urls) {
    $('#id_login').on('click', function() {
        navigator.id.request()
    })

    navigator.id.watch({
        loggedInUser: user,
        onlogin: function() {
            $.post(
                urls.login,
            ).fail(
                function() {
                    navigator.id.logout()
                }
            ).done(
                function() {
                    window.location.reload()
                }
            )
        },
        onlogout: function() {}
    })
}

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
}