from flask import Flask, request, render_template_string

app = Flask(__name__)

def fibonacci_in_range(start, end):
    """Generate Fibonacci numbers between start and end (inclusive)."""
    fibs = []
    a, b = 0, 1
    while a <= end:
        if start <= a <= end:
            fibs.append(a)
        a, b = b, a + b
    return fibs

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Fibonacci Range Finder</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #4a5568;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 20px;
            max-width: 400px;
            margin: 0 auto;
        }
        label {
            font-weight: bold;
            color: #2d3748;
            font-size: 1.1em;
        }
        input[type="number"] {
            padding: 15px;
            font-size: 1.2em;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        input[type="submit"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            font-size: 1.2em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.2s ease;
            font-weight: bold;
        }
        input[type="submit"]:hover {
            transform: translateY(-2px);
        }
        .error {
            background: #fed7d7;
            color: #c53030;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #e53e3e;
            margin: 20px 0;
        }
        .result {
            background: #c6f6d5;
            color: #22543d;
            padding: 25px;
            border-radius: 15px;
            margin-top: 30px;
            border-left: 5px solid #38a169;
        }
        .fib-list {
            background: white;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            line-height: 1.8;
            white-space: pre-wrap;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }
        .count {
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
            color: #2f855a;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔢 Fibonacci Range Finder</h1>
        <form method="POST">
            <label>Start Number:</label>
            <input type="number" name="start" value="{{ start or '' }}" required min="0">
            
            <label>End Number:</label>
            <input type="number" name="end" value="{{ end or '' }}" required min="0">
            
            <input type="submit" value="Generate Fibonacci Series ✨">
        </form>
        
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        
        {% if fibs %}
            <div class="result">
                <div class="count">Found {{ fibs|length }} Fibonacci numbers!</div>
                <div class="fib-list">{{ fibs }}</div>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    fib_result = []
    error = None
    start, end = '', ''
    
    if request.method == 'POST':
        try:
            start = int(request.form['start'])
            end = int(request.form['end'])
            if start > end:
                error = "❌ Start must be less than or equal to End"
            elif start < 0 or end < 0:
                error = "❌ Please enter non-negative numbers"
            else:
                fib_result = fibonacci_in_range(start, end)
                if not fib_result:
                    error = "No Fibonacci numbers found in this range"
        except ValueError:
            error = "❌ Please enter valid integers"
    
    return render_template_string(HTML_TEMPLATE, 
                                fibs=fib_result, 
                                start=start, 
                                end=end, 
                                error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  ### can be accessed from outside the docker container