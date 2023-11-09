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


def get_rss_update_notification_template(channel_name):
    return f"""
            <html>
            <body>
            <p>Hi !!! <br>{channel_name} has been updated</p>
            </body>
            </html>
            """


def template_mapper(arg, token):

    mapper = {
        "verify account": get_verify_template,
        "reset password": get_reset_password_template,
        "rss_update_notification": get_rss_update_notification_template
    }
    return mapper[arg](token)
