### INF601 - Advanced Programming in Python
### Corbin Luck
### Final Project

from flask import Blueprint, render_template, request as flask_request
from flaskr import api_URL, api_KEY
import requests

bp = Blueprint('search', __name__)

def search_cves(keyword, results_per_page=2000):
    params = {
        "keywordSearch": keyword,
        "resultsPerPage": str(results_per_page),
        "startIndex" : "0",
    }
    headers = {"apiKey": api_KEY} if api_KEY else {}

    try:
        response = requests.get(
            api_URL, params=params, headers=headers, timeout=15
        )
        response.raise_for_status()
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        total_results = data.get("totalResults", 0)

        cves = []
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "NONE": 0, "N/A": 0, "UNKNOWN": 0}
        scores = []

        for item in vulnerabilities:
            cve = item.get("cve", {})
            cve_id = cve.get("id", "N/A")

            description = "No description available"
            for desc in cve.get("descriptions", []):
                if desc.get("lang") == "en":
                    description = desc.get("value", description)
                    break
            score = None
            severity = None
            metrics = cve.get("metrics", {})
            for key in ["cvssMetricV31", "cvssMetricV30"]:
                if key in metrics and metrics[key]:
                    cvss_data = metrics[key][0].get("cvssData", {})
                    score = cvss_data.get("baseScore")
                    severity = cvss_data.get("baseSeverity") or metrics[key][0].get("baseSeverity")
                    break

            if severity:
                severity = severity.upper()
            else:
                severity = "N/A"

            published = cve.get("published", "")[:10]
            modified = cve.get("modified", "")[:10]

            refs = [
                r.get("url", "")
                for r in cve.get("references", [])[:2]
                if r.get("url")
            ]

            cves.append({
                "id": cve_id,
                "score": score,
                "description": description[:450] + "..." if len(description) > 450 else description,
                "severity": severity,
                "published": published,
                "modified": modified,
                "references": refs,
            })

            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            if score is not None:
                scores.append(score)
        average_score = round(sum(scores) / len(scores), 2) if scores else 0
        cves.sort(key=lambda x: (x["score"] is None, -(x["score"] or 0)))

        return {
            "cves": cves,
            "keyword": keyword,
            "total_results": total_results,
            "avg_score": average_score,
            "severity_counts": severity_counts,
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {"cves": [], "keyword": keyword, "error": "Request timed out. NVD API may be slow — try again.",
                "total_results": 0, "returned": 0, "avg_score": 0, "severity_counts": {}}
    except requests.exceptions.HTTPError as e:
        return {"cves": [], "keyword": keyword, "error": f"HTTP error: {e}", "total_results": 0, "returned": 0,
                "avg_score": 0, "severity_counts": {}}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"cves": [], "keyword": keyword, "error": str(e), "total_results": 0, "returned": 0, "avg_score": 0,
                "severity_counts": {}}

@bp.route('/search')
def search():
    keyword = flask_request.args.get('keyword', '').strip()

    if not keyword:
        return render_template("search.html", data=None, error="Please enter a keyword to search.")

    data = search_cves(keyword)
    return render_template("search.html", data=data)