from flask import Blueprint, render_template
from flaskr import api_URL, api_KEY
import requests

bp = Blueprint('low', __name__)

## Fetches the top 10 low severity CVEs ##
def get_low_severity():
    params = {
        "cvssV3Severity": "LOW",
        "resultsPerPage": "2000",
        "startIndex": "0",
    }
    headers = {"apiKey": api_KEY} if api_KEY else {}
    try:
        response = requests.get(api_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])

        cves = []
        score_buckets = {"0.0-1.9": 0, "2.0-3.9": 0, "4.0-5.9": 0}
        scores = []

        for item in vulnerabilities:
            cve = item.get("cve", {})
            cve_id = cve.get("id", "N/A")
            description = "No description available"
            for desc in cve.get("descriptions", []):
                if desc.get("lang") == "en":
                    description = desc.get("value", description)
                    break

            ## Extracts based on score ##
            score = None
            metrics = cve.get("metrics", {})
            for key in ["cvssMetricV31", "cvssMetricV30"]:
                if key in metrics and metrics[key]:
                    score = metrics[key][0]["cvssData"].get("baseScore")
                    break

            published = cve.get("published", "")[:10]

            cves.append({
                "id": cve_id,
                "description": description[:250] + "..." if len(description) > 250 else description,
                "score": score,
                "published": published,
            })

            if score is not None:
                scores.append(score)
                if score < 2.0:
                    score_buckets["0.0-1.9"] += 1
                elif score < 4.0:
                    score_buckets["2.0-3.9"] += 1
                else:
                    score_buckets["4.0-5.9"] += 1

        avg_score = round(sum(scores) / len(scores), 2) if scores else 0

        cves.sort(key=lambda x: (x["score"] is None, x["score"]))

        return {
        "cves": cves,
        "avg_score": avg_score,
        "score_buckets": score_buckets,
        "total": len(cves),
        }

    except Exception as e:
        return {"cves": [], "avg_score": 0, "score_buckets": {}, "total": 0, "error": str(e)}

@bp.route('/low')
def lowseverity():
    data = get_low_severity()
    return render_template('low.html', data=data)