QUnit.test("키를 입력할 때 에러가 숨겨져야 한다", function(assert) {
    $("input[name='text']").on('keypress', function() {
        $('.has-error').hide()
    })

    $("input[name='text']").trigger('keypress')
    assert.equal($('.has-error').is(':visible'), false)
})

QUnit.test("키 입력이 없으면 에러가 나온다", function(assert) {
    assert.equal($('.has-error').is(':visible'), true)
})
