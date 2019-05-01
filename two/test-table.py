from flask import Flask, render_template 
import pandas as pd
app = Flask(__name__)


@app.route("/")
def home():
    #return the html and the variable
    flies = [['Gold Ribbed Hares Ear', 18,16, 20], ['Purple Haze',14, 16, 12], ['Pheasant Tail',18, 20, 22]]
    test_table = pd.DataFrame(flies, columns = ['Fly', 'Best Size', 'Alternate Size', 'Last Resort Size']).to_html(table_id='best-flies')
    return render_template('index2.html', test_table=test_table)


if __name__ == "__main__":
    app.run(debug=True)