from flask import Flask, render_template, request, jsonify
import requests
from checker import fetch_page, run_checks

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        soup, final_url = fetch_page(url)
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Could not connect to {url}. Check the URL and try again."}), 400
    except requests.exceptions.Timeout:
        return jsonify({"error": "The request timed out. The site may be slow or unreachable."}), 400
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"HTTP error: {e.response.status_code} {e.response.reason}."}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to fetch page: {str(e)}"}), 400

    issues, manual_checks, js_rendered = run_checks(soup)

    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    return jsonify({
        "url": final_url,
        "js_rendered": js_rendered,
        "total_issues": len(issues),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "issues": issues,
        "manual_checks": manual_checks,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
