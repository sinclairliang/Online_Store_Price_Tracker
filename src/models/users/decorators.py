def requires_login(func):
    func()


@requires_login
def my_function():
    print("Hello World")
    return "Hi"
