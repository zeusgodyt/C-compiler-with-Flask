from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile():
    code = request.form['code']
    input_data = request.form['input']
    
    with open('temp.c', 'w') as f:
        f.write(code)

    with open('input.txt', 'w') as f:
        f.write(input_data)

    # Compilation and execution with MiniGW Compiler
    compilation_result = subprocess.run(['gcc', 'temp.c', '-o', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if compilation_result.returncode == 0:
        execution_result = subprocess.run(['./temp'], stdin=open('input.txt'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = execution_result.stdout.decode()
        error = execution_result.stderr.decode()
    else:
        output = ''
        error = compilation_result.stderr.decode()
    
    return render_template('index.html', output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
