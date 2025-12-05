from flask import Flask, render_template, request, redirect, send_file
from extractor.berlin import extract_berlin_jobs
from extractor.web3 import extract_web3_jobs
from extractor.wwr import extract_wwr_jobs
from file import save_to_file

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}

app = Flask("JobScraper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == "":
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        berlin = extract_berlin_jobs(keyword, headers)
        web3 = extract_web3_jobs(keyword, headers)
        wwr = extract_wwr_jobs(keyword)
        jobs = berlin + web3 + wwr
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs, total=len(jobs))

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == "":
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run(debug=True)