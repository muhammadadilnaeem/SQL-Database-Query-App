from flask import Flask, render_template, request, redirect, url_for, flash
from langchain_community.llms import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Chatwithsql:
    def __init__(self, db_user, db_password, db_host, db_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_name = db_name

    def message(self, query):
        llm = OpenAI(model_name="gpt-3.5-turbo", api_key="your_secret_key")
        db = SQLDatabase.from_uri(f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}")
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
        result = agent_executor.run(query)
        return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db_user = request.form['db_user']
        db_password = request.form['db_password']
        db_host = request.form['db_host']
        db_name = request.form['db_name']
        query = request.form['query']

        try:
            db = Chatwithsql(db_user, db_password, db_host, db_name)
            result = db.message(query)
            return render_template('result.html', result=result)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
