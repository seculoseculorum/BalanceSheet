from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__)

# ----------------------------
# Loan amortization calculator
# ----------------------------

def amortized_loan_schedule(principal, annual_rate, years, payments_per_year=12):
    r = annual_rate / payments_per_year
    n = int(years * payments_per_year)

    payment = principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

    schedule = []
    balance = principal

    for i in range(1, n + 1):
        interest = balance * r
        principal_payment = payment - interest
        balance -= principal_payment
        balance = max(balance, 0)

        schedule.append({
            "payment_number": i,
            "payment": round(payment, 2),
            "principal_paid": round(principal_payment, 2),
            "interest_paid": round(interest, 2),
            "remaining_balance": round(balance, 2)
        })

    return schedule


# ----------------------------
# Loan calculator route
# ----------------------------

@app.route("/loan", methods=["GET", "POST"])
def loan_calculator():
    schedule = None

    if request.method == "POST":
        try:
            principal = float(request.form.get("principal", 0))
            annual_rate = float(request.form.get("annual_rate", 0)) / 100
            years = float(request.form.get("years", 0))
            payments_per_year = int(request.form.get("ppy", 12))

            schedule = amortized_loan_schedule(
                principal, annual_rate, years, payments_per_year
            )

        except ValueError:
            schedule = []

    return render_template("loan.html", schedule=schedule)


# ----------------------------
# Tase-laskuri (main calculator)
# ----------------------------

@app.route("/tase", methods=["GET", "POST"])
def tase_laskuri():
    result = None
    error = None
    rows = []

    if request.method == "POST":
        try:
            names = request.form.getlist("name[]")
            classes = request.form.getlist("class[]")
            book_values = request.form.getlist("book_value[]")
            market_values = request.form.getlist("market_value[]")
            comments = request.form.getlist("comment[]")

            total_assets_book = 0
            total_assets_market = 0
            total_liabilities_book = 0
            total_liabilities_market = 0

            rows = []

            for i in range(len(names)):
                row = {
                    "name": names[i],
                    "class": classes[i],
                    "book_value": float(book_values[i] or 0),
                    "market_value": float(market_values[i] or 0),
                    "comment": comments[i]
                }
                rows.append(row)

                if classes[i].lower() in ["asset", "vara"]:
                    total_assets_book += row["book_value"]
                    total_assets_market += row["market_value"]
                elif classes[i].lower() in ["liability", "velka"]:
                    total_liabilities_book += row["book_value"]
                    total_liabilities_market += row["market_value"]

            # ✅ Define lists for treemap
            assets = [r for r in rows if r["class"].lower() in ["asset", "vara"]]
            liabilities = [r for r in rows if r["class"].lower() in ["liability", "velka"]]

            # ✅ Build result
            result = {
                "total_assets_book": total_assets_book,
                "total_assets_market": total_assets_market,
                "total_liabilities_book": total_liabilities_book,
                "total_liabilities_market": total_liabilities_market,
                "equity_book": total_assets_book - total_liabilities_book,
                "equity_market": total_assets_market - total_liabilities_market,
                "assets": assets,
                "liabilities": liabilities
            }

        except ValueError:
            error = "Please enter valid numeric values for Book and Market value."

    return render_template("tase.html", result=result, error=error, rows=rows)


# ----------------------------
# New main menu route
# ----------------------------

@app.route("/")
def main_index():
    return render_template("index.html")


# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
