# cypy - UI generator.
# ===================================

username = "Username:<br><input type='text' name='username'><br>"
password = "Password:<br><input type='password' name='password'><br>"
keyword = "Keyword:<br><input type='password' name='keyword'><br><br>"
submit = "<input type='submit' value='Submit'>"
page = "<html><head><title>CyPy</title></head><body>{}</body></html>"


def enclose(block, element):
    return "<" + element + ">" + block + "</" + element + ">"


def generate_form(action):
    if action == "/add":
        form_body = enclose(username + password + keyword + submit, "fieldset")
    elif action == "/get":
        form_body = enclose(username + keyword + submit, "fieldset")
    elif action == "/del":
        form_body = enclose(username + keyword + submit, "fieldset")
    else:
        raise ValueError("No valid action chosen.")
    form = ("<form action='{0}' method='post'>{1}</form>".format(action,
                                                                 form_body))
    return page.format(form)
