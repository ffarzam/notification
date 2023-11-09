def get_verify_template(token):
    return f"""
            <html>
            <body>
            <p>Hi !!! <br>your code to verify your account: {token}</p>
            </body>
            </html>
            """


def get_reset_password_template(token):
    return f"""
            <html>
            <body>
            <p>Hi !!! <br>your code to reset your password: {token}</p>
            </body>
            </html>
            """


def template_mapper(arg, token):

    mapper = {
        "verify account": get_verify_template,
        "reset password": get_reset_password_template,
    }
    return mapper[arg](token)
