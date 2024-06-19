style_html = """
        <style>
            button{margin:0.2em}
            html{font-family:'Open Sans', sans-serif;margin:2%}
            table{width:80%;max-width:100%;margin-bottom:1em;border-collapse:collapse}
            body{display: flex;flex-direction: column;align-items: center;margin: 0;}
            form{width:100%}
            textarea{width:100%}
        </style>
"""

payload_html = """<html>
    <head>
        <title>Pico W Ducky</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {}
    </head>
    <body>
        <h1>Pico W Ducky</h1>
        <table border="1"><tr><th>Payload</th><th>Actions</th></tr>{}</table><br>
        <a href="/new"><button>New Script</button></a>
        <a href="/enableStorage"><button>Enable Storage</button></a>
    </body>
</html>
"""

edit_html = """<!DOCTYPE html>
<html> 
    <head>
        <title>Script Editor</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {}
    </head>
    <body>
        <form action="/write/{}" method="POST">
            <textarea rows="20" name="scriptData">{}</textarea><br/>
            <input type="submit" value="Submit"/>
        </form>
        <br>
        <a href="/ducky"><button>Home</button></a>
    </body>
</html>
"""

new_html = """<!DOCTYPE html>
<html>
    <head>
        <title>New Script</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {}  
    </head>
    <body>
            <form action="/new" method="POST">
                <p>New Script:</p>
                <textarea rows="1" name="scriptName" placeholder="script name"></textarea><br>
                <textarea id="ducky-input" rows="20" name="scriptData" placeholder="script"></textarea>
                <br><input type="submit" value="Submit"/>
            </form>
            <a href="/ducky"><button>Go Back</button></a>
    </body>
</html>
"""

response_html = """<!DOCTYPE html>
<html>
    <head>
        <title>Pico W Ducky</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
       {}
    </head>
    <body>
        <h1>Pico W Ducky</h1>
        {}
        <br><a href="/ducky"><button>Home</button></a>
    </body>
</html>
"""

newrow_html = """
            <tr>
                <td>{}</td>
                <td>
                    <a href='/edit/{}'><button>Edit</button></a>
                    <a href='/run/{}'><button>Run</button></a>
                    <a href='/delete/{}'><button>Delete</button></a>
                </td>
            </tr>
            """