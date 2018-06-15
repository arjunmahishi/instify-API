from flask import Flask, request, render_template
import pprint
import erp

app = Flask(__name__)
pp = pprint.PrettyPrinter(indent=4)

@app.route('/', methods=['POST', 'GET'])
def hello():
    # print request.form.to_dict(flat=False)

    if request.method == "GET":
        return erp.login("ra1511008020111", "dps12345")

    else:
        pp.pprint(request.form.to_dict(flat=False))
        return "erp.login()"

if __name__ == '__main__':
    app.run(debug=True)
