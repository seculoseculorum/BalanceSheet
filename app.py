from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    rows = []

    if request.method == "POST":
        try:
            # Get data from form
            names = request.form.getlist("name[]")
            classes = request.form.getlist("class[]")
            book_values = request.form.getlist("book_value[]")
            market_values = request.form.getlist("market_value[]")
            comments = request.form.getlist("comment[]")

            total_assets_book = 0
            total_assets_market = 0
            total_liabilities_book = 0
            total_liabilities_market = 0

            # Build row data and calculate totals
            for i in range(len(names)):
                row = {
                    "name": names[i],
                    "class": classes[i],
                    "book_value": float(book_values[i] or 0),
                    "market_value": float(market_values[i] or 0),
                    "comment": comments[i]
                }
                rows.append(row)

                if classes[i].lower() == "asset":
                    total_assets_book += row["book_value"]
                    total_assets_market += row["market_value"]
                elif classes[i].lower() == "liability":
                    total_liabilities_book += row["book_value"]
                    total_liabilities_market += row["market_value"]

            result = {
                "total_assets_book": total_assets_book,
                "total_assets_market": total_assets_market,
                "total_liabilities_book": total_liabilities_book,
                "total_liabilities_market": total_liabilities_market,
                "equity_book": total_assets_book - total_liabilities_book,
                "equity_market": total_assets_market - total_liabilities_market
            }

        except ValueError:
            error = "Please enter valid numeric values for Book and Market value."

    return render_template("index.html", result=result, error=error, rows=rows)

if __name__ == "__main__":
    app.run(debug=True)