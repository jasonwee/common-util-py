
from mailer import is_email_address_valid

# https://gist.github.com/cjaoude/fd9910626629b53c4d25


def test_valid_email():
    assert is_email_address_valid("email@example.com")
    assert is_email_address_valid("firstname.lastname@example.com")
    assert is_email_address_valid("email@subdomain.example.com")
    assert is_email_address_valid("firstname+lastname@example.com")
    assert is_email_address_valid("email@123.123.123.123")
    assert is_email_address_valid("email@[123.123.123.123]")
    assert is_email_address_valid('"email"@example.com')
    assert is_email_address_valid("1234567890@example.com")
    assert is_email_address_valid("email@example-one.com")
    assert is_email_address_valid("_______@example.com")
    assert is_email_address_valid("email@example.name")
    assert is_email_address_valid("email@example.museum")
    assert is_email_address_valid("email@example.co.jp")
    assert is_email_address_valid("firstname-lastname@example.com")
    # much.”more\ unusual”@example.com
    assert is_email_address_valid("much.”more\\ unusual”@example.com")
    assert is_email_address_valid("very.unusual.”@”.unusual.com@example.com")
    assert is_email_address_valid('very.”(),:;<>[]”.VERY.”very@\\ "very”.unusual@strange.example.com')

def test_invalid_email():
    assert not is_email_address_valid("plainaddress")
    assert not is_email_address_valid("#@%^%#$@#$@#.com")
    assert not is_email_address_valid("@example.com")
    #assert not is_email_address_valid("Joe Smith <email@example.com>")
    assert not is_email_address_valid("email.example.com")
    assert not is_email_address_valid("email@example@example.com")
    #assert not is_email_address_valid(".email@example.com")
    #assert not is_email_address_valid("email.@example.com")
    #assert not is_email_address_valid("email..email@example.com")
    #assert not is_email_address_valid("あいうえお@example.com")
    #assert not is_email_address_valid("email@example.com (Joe Smith)")
    assert not is_email_address_valid("email@example")
    #assert not is_email_address_valid("email@-example.com")
    #assert not is_email_address_valid("email@example.web")
    #assert not is_email_address_valid("email@111.222.333.44444")
    #assert not is_email_address_valid("email@example..com")
    #assert not is_email_address_valid("Abc..123@example.com")
    #assert not is_email_address_valid("”(),:;<>[\]@example.com")
    #assert not is_email_address_valid("just”not”right@example.com")
    #assert not is_email_address_valid('this\ is"really"not\allowed@example.com')
    assert not is_email_address_valid("'''")
