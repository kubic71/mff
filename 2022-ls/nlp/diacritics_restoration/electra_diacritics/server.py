from inference import load_model, diacritize

# simple server serving the torch model

# simple html site with input and a button
page = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Diacritizer</title>
  <meta name="description" content="Diacritizer">
  <meta name="author" content="">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
  <h2>Diacritizer</h2>
  <form action="/" method="post">
    <div class="form-group">
      <label for="text">Text:</label>
    <!--- The text field should be multi-line ---> 
      <textarea class="form-control" rows="5" id="text" name="text">Vyzkousej me, zkusim ti dopsat hacky a carky tam, kde ti budou chybet!</textarea>
    </div>
    <button type="submit" class="btn btn-default">Submit</button>
  </form>
  <div id="output"></div>
</div>

<script>
$(document).ready(function(){
  $("form").submit(function(event){
    event.preventDefault();
    $.ajax({
      url: "/",
      type: "POST",
      data: $("form").serialize(),
      success: function(response){
        $("#output").html(response);
      }
    });
  });
});
</script>

</body>
</html>
"""

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="larger-100k_epoch_41")
    parser.add_argument("--n-iters", type=int, default=2)
    parser.add_argument("--port", type=int, default=8080)

    args = parser.parse_args()

    model = load_model(args.checkpoint)


    import flask
    from io import StringIO

    app = flask.Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if flask.request.method == "POST":
            text = flask.request.form["text"]
            # diacritize(input: TextIO, output: TextIO, model: DiacriticModel, n_iters: int = 1, use_dict=True):
            output_stream = StringIO()
            diacritize(StringIO(text), output_stream, model, args.n_iters, True)

            return output_stream.getvalue()

        return page

    print("Click here to open the web server: http://localhost:{}".format(args.port))
    app.run(port=args.port)
